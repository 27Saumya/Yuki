from ..config import pastebin_api_key


async def create_guest_paste_bin(session, code):
    res = await session.post(
        "https://pastebin.com/api/api_post.php",
        data={
            "api_dev_key": pastebin_api_key,
            "api_paste_code": code,
            "api_paste_private": 0,
            "api_paste_name": "output.txt",
            "api_paste_expire_date": "1D",
            "api_option": "paste",
        },
    )
    return await res.text()