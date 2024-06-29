slack의 아래 Notification 템플릿과 Python Error 클래스 구조를 제공합니다. 에러 클래스를 Slack에서 보기 쉽게 구조화 해주세요.

Notification 템플릿
```json
{
	"blocks": [
		{
			"type": "section",
			"text": {
				"type": "plain_text",
				"emoji": true,
				"text": "Looks like you have a scheduling conflict with this event:"
			}
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*<fakeLink.toUserProfiles.com|Iris / Zelda 1-1>*\nTuesday, January 21 4:00-4:30pm\nBuilding 2 - Havarti Cheese (3)\n2 guests"
			},
			"accessory": {
				"type": "image",
				"image_url": "https://api.slack.com/img/blocks/bkb_template_images/notifications.png",
				"alt_text": "calendar thumbnail"
			}
		},
		{
			"type": "context",
			"elements": [
				{
					"type": "image",
					"image_url": "https://api.slack.com/img/blocks/bkb_template_images/notificationsWarningIcon.png",
					"alt_text": "notifications warning icon"
				},
				{
					"type": "mrkdwn",
					"text": "*Conflicts with Team Huddle: 4:15-4:30pm*"
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Propose a new time:*"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Today - 4:30-5pm*\nEveryone is available: @iris, @zelda"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"emoji": true,
					"text": "Choose"
				},
				"value": "click_me_123"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Tomorrow - 4-4:30pm*\nEveryone is available: @iris, @zelda"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"emoji": true,
					"text": "Choose"
				},
				"value": "click_me_123"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*Tomorrow - 6-6:30pm*\nSome people aren't available: @iris, ~@zelda~"
			},
			"accessory": {
				"type": "button",
				"text": {
					"type": "plain_text",
					"emoji": true,
					"text": "Choose"
				},
				"value": "click_me_123"
			}
		},
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": "*<fakelink.ToMoreTimes.com|Show more times>*"
			}
		}
	]
}
```

Python 에러 클래스
```python
class APIStatusError(APIError):
    """Raised when an API response has a status code of 4xx or 5xx."""

    response: httpx.Response
    status_code: int
    request_id: str | None


class APIError(OpenAIError):
    message: str
    request: httpx.Request

    body: object | None
    """The API response body.

    If the API responded with a valid JSON structure then this property will be the
    decoded result.

    If it isn't a valid JSON structure then this will be the raw response.

    If there was no response associated with this error then it will be `None`.
    """

    code: Optional[str] = None
    param: Optional[str] = None
    type: Optional[str]
```

에러 클래스에서 message, code, status_code, request_id 위주로 구조화 되면 좋을것 같습니다