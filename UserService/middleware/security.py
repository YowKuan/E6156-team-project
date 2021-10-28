import json

unsecure_paths = []

def security_check(request, google, blueprint):
    path = request.path
    result = False

    if path in unsecure_paths:
        result = True
    else:
        google_data = None

        user_info_endpoint = '/oauth2/v2/userinfo'

        if google.authorized:
            google_data = google.get(user_info_endpoint).json()
            print(json.dumps(google_data, indent=2))

            s = blueprint.session
            t = s.token
            print("Token", json.dumps(t, indent=2))

            result = True
             
    return result

