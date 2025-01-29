import requests

class ApiClient:
    def __init__(self):
        """
        Initialize the API client with a base URL.
        """

    def send_otp(self, otp, user_id, title="foo", body="bar"):
        """
        Sends a POST request to the API with OTP and other payload data.

        :param otp: The OTP to send in the payload.
        :param user_id: The user ID to include in the payload.
        :param title: The title for the payload (default: "foo").
        :param body: The body for the payload (default: "bar").
        :return: The API response as a dictionary or an error message.
        """
        # Construct the URL
        url = f"{self.base_url}/posts"

        # Payload with OTP
        payload = {
            "title": title,
            "body": body,
            "userId": user_id,
            "otp": otp  # Adding OTP to the payload
        }

        try:
            # Sending POST Request
            response = requests.post(url, json=payload)

            # Check response status
            if response.status_code == 201:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": f"Failed with status code {response.status_code}"}
        except requests.exceptions.RequestException as e:
            return {"success": False, "error": str(e)}

# Usage example
if __name__ == "__main__":
    # Initialize the API client
    client = ApiClient(base_url="api/communication/send-email/")

    # Send OTP
    result = client.send_otp(otp=123456, user_id=1)

    # Print the result
    if result["success"]:
        print("Response Data:", result["data"])
    else:
        print("Error:", result["error"])
