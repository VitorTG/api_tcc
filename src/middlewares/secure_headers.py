import secure


class SecureHeaders:
    def process_request(self, req, resp):
        csp = secure.ContentSecurityPolicy().default_src("'self'")
        xxp = secure.XXSSProtection().set("1; mode=block")
        secure_headers = secure.Secure(csp=csp, xxp=xxp)

        secure_headers.framework.falcon(resp)
