package api

type Session struct {
	ID                 int    `db:"id"`
	Name               string `db:"ssn"`
	SessionSecret      string `db:"session_secret"`
	ChefsgradeApproved bool   `db:"chefsgradde_approved"`
}

func (s *service) GetSession(id string) (*Session, error) {
	row := s.db.QueryRow("SELECT id, name, session_secret, chefsgradde_approved FROM sessions WHERE session_secret = $1", id)
	if row.Err() != nil {
		return nil, row.Err()
	}

	var u Session
	err := row.Scan(&u.ID, &u.Name, &u.SessionSecret, &u.ChefsgradeApproved)
	if err != nil {
		return nil, err
	}

	return &u, nil
}

func (s *service) CreateSession(name, session_secret string) error {
	_, err := s.db.Exec("insert into sessions (name, session_secret, chefsgradde_approved) VALUES ($1, $2, $3)", name, session_secret, false)
	return err
}

func (s *service) AllowChefsgrädde(session_secret string) error {
	_, err := s.db.Exec("UPDATE sessions SET chefsgradde_approved = TRUE WHERE session_secret = $1", session_secret)
	return err
}
