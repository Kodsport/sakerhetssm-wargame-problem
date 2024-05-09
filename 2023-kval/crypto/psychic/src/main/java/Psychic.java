import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServlet;
import jakarta.servlet.http.HttpServletRequest;
import jakarta.servlet.http.HttpServletResponse;
import jakarta.servlet.ServletException;
import java.io.IOException;
import java.security.InvalidKeyException;
import java.security.KeyFactory;
import java.security.NoSuchAlgorithmException;
import java.security.Signature;
import java.security.SignatureException;
import java.security.interfaces.ECPrivateKey;
import java.security.interfaces.ECPublicKey;
import java.security.spec.InvalidKeySpecException;
import java.security.spec.PKCS8EncodedKeySpec;
import java.security.spec.X509EncodedKeySpec;
import java.util.Base64;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class Psychic extends HttpServlet {
	private static final long serialVersionUID = 1L;

	private static String FLAG = System.getenv("FLAG") != null ? System.getenv("FLAG") : "sentor_temp_flag";

    private static ECPublicKey EC_PUBLIC_KEY;
    private static ECPrivateKey EC_PRIVATE_KEY;
    
    public Psychic() throws RuntimeException, NoSuchAlgorithmException, InvalidKeySpecException {
		super();
		final KeyFactory keyPairGenerator = KeyFactory.getInstance("EC");
		if (System.getenv("PUBLIC_KEY") != null && System.getenv("PRIVATE_KEY") != null) {
			EC_PUBLIC_KEY = (ECPublicKey) keyPairGenerator.generatePublic(new X509EncodedKeySpec(Base64.getDecoder().decode(System.getenv("PUBLIC_KEY"))));
			EC_PRIVATE_KEY = (ECPrivateKey) keyPairGenerator.generatePrivate(new PKCS8EncodedKeySpec(Base64.getDecoder().decode(System.getenv("PRIVATE_KEY"))));
		} else {
			throw new RuntimeException("Error: Need to set PUBLIC_KEY and PRIVATE_KEY environmental variables.");
		}
    }
    
    /*
     * Parse through the available cookies to find our authentication cookie
     */
	private String getAuthCookie(Cookie[] cookies) {
		if (cookies == null) {
			return null;
		}
        for (int i = 0; i < cookies.length; i++) {
            if (cookies[i].getName().equals("auth")) {
            	return cookies[i].getValue();
            }
         }
		return null;
	}
    
	/*
	 * Generate a new JWT from hardcoded values, only The Doctor is able to impersonate anyone else
	 */
	protected String generateJwt() {
		String header = "{\"alg\":\"ES256\",\"typ\":\"JWT\"}";
		String payload = "{\"sub\":\"the_doctor\",\"iss\":\"tardis\",\"nbf\":1678474800,\"exp\":1678647600,\"iat\":" + String.valueOf(System.currentTimeMillis() / 1000) + "}";

        String headerStr = Base64.getUrlEncoder().withoutPadding().encodeToString(header.getBytes());
        String payloadStr = Base64.getUrlEncoder().withoutPadding().encodeToString(payload.getBytes());

        Signature signature;
		try {
			signature = Signature.getInstance("SHA256withECDSAinP1363Format");
	        signature.initSign(EC_PRIVATE_KEY);
	        signature.update((headerStr + "." + payloadStr).getBytes());
	
	        byte[] signatureBytes = signature.sign();
	        String signatureStr = Base64.getUrlEncoder().withoutPadding().encodeToString(signatureBytes);
	
	        String jwt = headerStr + "." + payloadStr + "." + signatureStr;
	        return jwt;
		} catch (NoSuchAlgorithmException | InvalidKeyException | SignatureException e) {
			return "Error: Couldn't generate JWT";
		}
	}

	/*
	 * Validate the JWT.
	 * 
	 * Just validate the cryptographic signature, this is safe enough.
	 */
	protected Boolean validateJwt(String jwtStr) throws RuntimeException {
		var splitJwt = jwtStr.split("\\.");
		if (splitJwt.length != 3) {
			throw new RuntimeException("Unable to parse JWT");
		}

		var headerB64 = splitJwt[0];
		var payloadB64 = splitJwt[1];
		var signatureB64 = splitJwt[2];
		
		try {
			var signature = Signature.getInstance("SHA256withECDSAinP1363Format");
			signature.initVerify(EC_PUBLIC_KEY);
			signature.update((headerB64 + "." + payloadB64).getBytes());
			if (!signature.verify(Base64.getUrlDecoder().decode(signatureB64))) {
				throw new RuntimeException("Invalid signature");
			}
			return true;
		} catch (NoSuchAlgorithmException | InvalidKeyException | SignatureException e) {
			throw new RuntimeException("Unable to validate signature", e);
		}
	}
	
	/*
	 * Parse the JWT and return the subject name.
	 * 
	 * Important: need to be validated before!
	 */
	protected String parseJwt(String jwtStr) {
		var splitJwt = jwtStr.split("\\.");
		if (splitJwt.length != 3) {
			throw new RuntimeException("Unable to parse JWT");
		}

		var payloadB64 = splitJwt[1];
        final String payloadStr = new String(Base64.getUrlDecoder().decode(payloadB64));
		
        Pattern p = Pattern.compile("\"sub\":\\s*\"([^\"]+)\"");
	    Matcher m = p.matcher(payloadStr);
	    if (m.find()) {
	    	return m.group(1);
	    } else {
	    	throw new RuntimeException("Unable to parse subject");
	    }
	}

	/*
	 * Serve the web page
	 */
	protected void doGet(HttpServletRequest request, HttpServletResponse response) throws ServletException, IOException {
		String jwtStr;
		String cookie = getAuthCookie(request.getCookies());
		if (cookie == null) {
			jwtStr = generateJwt();
			Cookie authCookie = new Cookie("auth", generateJwt());
			response.addCookie(authCookie);
		} else {
			jwtStr = cookie;
		}
		
		String message = "";
		try {
			if (validateJwt(jwtStr)) {
				String user = parseJwt(jwtStr);
				message = "Welcome " + user + "!\n";
				if (user.equals("the_master")) {
					message += "Your flag is: " + FLAG;
				} else {
					message += "Only the_master can access the flag";
				}
			}
			else {
				message = "Invalid JWT token";
			}
		} catch (RuntimeException e) {
			message = "Error: " + e.getMessage();
		}
		
		response.getWriter().append(message);
	}
}