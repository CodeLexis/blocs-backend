class Dialogue(object):
    @classmethod
    def __wrap_quick_reply_option(cls, text=None, payload=None, image_url=None,
                                  template=None):

        if template:
            return {"content_type": template}

        wrap = {"content_type": "text", "title": text, "payload": payload}

        if image_url is not None:
            wrap['image_url'] = image_url

        return wrap

    @classmethod
    def quick_reply(cls, title, texts_and_payloads):
        replies = []

        for text, payload in texts_and_payloads:
            qr = cls.__wrap_quick_reply_option(text, payload)
            replies.append(qr)

        return (title, replies)

    @classmethod
    def button(cls, type, title, payload=None, url=None):
        result = {'type': type, 'title': title}

        if payload is not None:
            result['payload'] = payload

        elif url is not None:
            result['url'] = url

        return result

    @classmethod
    def generic(cls, title, subtitle, image_url, buttons, url=None):
        results = {
            "title": title,
            "image_url": image_url,
            "subtitle": subtitle,
            "buttons": buttons
        }

        if url is not None:
            results["default_action"] = {
                "type": "web_url",
                "messenger_extensions": False,
                "webview_height_ratio": "tall",
                "url": url
            }

        return results

    @classmethod
    def get_location(self):
        raise NotImplementedError()
