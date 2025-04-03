package api

import (
	"database/sql"
	"encoding/base64"
	"net/http"
	"sync"
	"time"

	"github.com/Kansuler/bankid"
	"github.com/gin-gonic/gin"
	"github.com/google/uuid"
)

type service struct {
	db  *sql.DB
	bid *bankid.BankID

	lock         sync.RWMutex
	transactions map[string]authSignResponse
}

type authSignResponse struct {
	QrStartToken  string `json:"qrStartToken"`
	QrStartSecret string `json:"qrStartSecret"`

	// added fields
	startedAt time.Time
}

func New(db *sql.DB, bid *bankid.BankID) *service {
	srv := &service{
		db:           db,
		bid:          bid,
		transactions: map[string]authSignResponse{},
	}
	go srv.pruneCache()
	return srv
}

func (s *service) pruneCache() {

	t := time.NewTicker(time.Second * 30)

	for range t.C {

		s.lock.Lock()

		for k, asr := range s.transactions {
			if time.Since(asr.startedAt).Minutes() >= 5 {
				delete(s.transactions, k)
			}
		}

		s.lock.Unlock()
	}
}

func (s *service) Logout(c *gin.Context) {
	c.SetCookie("sockerstoppkaka", "", 0, "/", "", true, true)
	c.AbortWithStatus(200)
}

func (s *service) GräddeEula(c *gin.Context) {

	res, err := s.bid.Sign(c, bankid.SignOptions{
		EndUserIp:       c.ClientIP(),
		UserVisibleData: base64.RawStdEncoding.EncodeToString([]byte("Jag lovar med heder och samvete att inte missbruka makten som chefsgrädden bringar.")),
		Requirement: &bankid.Requirement{
			CertificatePolicies: []string{"1.2.752.78.1.5"},
		},
	})

	if err != nil {
		c.AbortWithStatusJSON(http.StatusInternalServerError, gin.H{
			"status": ":(",
			"err":    err.Error(),
		})
		return
	}

	s.lock.Lock()
	s.transactions[res.OrderRef] = authSignResponse{
		QrStartToken:  res.QrStartToken,
		QrStartSecret: res.QrStartSecret,
		startedAt:     time.Now(),
	}
	s.lock.Unlock()

	qr, _ := bankid.Qr(res.QrStartToken, res.QrStartSecret, 0)

	c.JSON(http.StatusOK, gin.H{
		"order_ref": res.OrderRef,
		"qr_code":   qr,
	})

}

func (s *service) CollectGräddeEula(c *gin.Context) {

	var r struct {
		OrderRef string `json:"order_ref"`
	}
	err := c.BindJSON(&r)
	if err != nil {
		return
	}

	s.lock.Lock()
	defer s.lock.Unlock()

	x, ok := s.transactions[r.OrderRef]
	if !ok {
		c.AbortWithStatus(http.StatusBadRequest)
		return
	}

	res, err := s.bid.Collect(c, bankid.CollectOptions{
		OrderRef: r.OrderRef,
	})

	if err != nil {
		c.AbortWithError(http.StatusInternalServerError, err)
		return
	}

	if res.Status == bankid.Pending {
		qr, _ := bankid.Qr(x.QrStartToken, x.QrStartSecret, int64(time.Since(x.startedAt).Seconds()))

		c.JSON(200, gin.H{
			"qr_code": qr,
			"status":  "pending",
		})
		return
	}

	if res.Status == bankid.Complete {
		id, _ := c.Cookie("sockerstoppkaka")
		err := s.AllowChefsgrädde(id)
		if err != nil {
			c.AbortWithError(http.StatusInternalServerError, err)
			return
		}
	}

}

func (s *service) BankIDAuth(c *gin.Context) {
	var r struct {
		Ssn string `json:"ssn"`
	}
	err := c.BindJSON(&r)
	if err != nil {
		return
	}

	if len(r.Ssn) != 12 {
		c.AbortWithStatusJSON(400, "invalid ssn")
		return
	}

	res, err := s.bid.Auth(c, bankid.AuthOptions{
		EndUserIp: c.ClientIP(),
		Requirement: bankid.Requirement{
			PersonalNumber: r.Ssn,
		},
	})

	if err != nil {
		c.AbortWithError(500, err)
		return
	}

	s.lock.Lock()
	s.transactions[res.OrderRef] = authSignResponse{
		QrStartToken:  res.QrStartToken,
		QrStartSecret: res.QrStartSecret,
		startedAt:     time.Now(),
	}
	s.lock.Unlock()

	qr, _ := bankid.Qr(res.QrStartToken, res.QrStartSecret, 0)
	c.JSON(200, gin.H{
		"qr_code":   qr,
		"order_ref": res.OrderRef,
	})
}

func (s *service) BankIDCollect(c *gin.Context) {

	var r struct {
		OrderRef string `json:"order_ref"`
	}
	err := c.BindJSON(&r)
	if err != nil {
		return
	}

	s.lock.Lock()
	defer s.lock.Unlock()

	x, ok := s.transactions[r.OrderRef]

	if !ok {
		c.AbortWithStatus(404)
		return
	}

	res, err := s.bid.Collect(c, bankid.CollectOptions{
		OrderRef: r.OrderRef,
	})
	if err != nil {
		c.JSON(500, gin.H{
			"error": err.Error(),
		})
		return
	}

	if res.Status == bankid.Failed {
		delete(s.transactions, r.OrderRef) // ta bort?

		c.JSON(200, gin.H{
			"status": "failed",
		})
		return
	}

	if res.Status == bankid.Pending {

		qr, _ := bankid.Qr(x.QrStartToken, x.QrStartSecret, int64(time.Since(x.startedAt).Seconds()))

		c.JSON(200, gin.H{
			"qr_code": qr,
			"status":  "pending",
		})
		return
	}

	if res.Status != bankid.Complete {
		// unknown status
		c.AbortWithStatus(500)
		return
	}

	delete(s.transactions, r.OrderRef)

	id := uuid.NewString()
	err = s.CreateSession(res.CompletionData.User.Name, id)
	if err != nil {
		c.AbortWithError(http.StatusInternalServerError, err)
		return
	}

	c.SetCookie("sockerstoppkaka", id, 0, "/", "", false, false)
	c.JSON(200, gin.H{
		"Status": "complete",
	})
}
