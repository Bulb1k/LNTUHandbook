import aiohttp
from bs4 import BeautifulSoup
from typing import Optional, List, Dict


class LntuTeacherClient:
    BASE_URL = "https://rating2.lntu.edu.ua"
    SEARCH_PATH = "/uk/searchuser"

    @staticmethod
    async def get_faculties() -> List[Dict[str, str]]:
        """
        Повертає список кафедр із їхніми ID та назвами,
        бере із <select name="combine"> на сторінці /uk/searchuser.
        """
        url = f"{LntuTeacherClient.BASE_URL}{LntuTeacherClient.SEARCH_PATH}"
        headers = {"User-Agent": "Mozilla/5.0"}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as resp:
                html = await resp.text()

        soup = BeautifulSoup(html, "html.parser")
        faculties: List[Dict[str, str]] = []

        select = soup.find("select", attrs={"name": "combine"})
        if not select:
            return faculties

        for option in select.find_all("option"):
            value = option.get("value", "").strip()
            name = option.get_text(strip=True)
            if value and name and value.lower() != "all":
                faculties.append({"id": value, "name": name})

        return faculties

    @staticmethod
    async def get_teachers(combine: Optional[str] = None) -> List[Dict[str, str]]:
        """
        Повертає список викладачів із /uk/searchuser?combine={combine}.
        Якщо combine не вказаний, вертає всіх (- Усі -).
        """
        params = {}
        if combine:
            params["combine"] = combine

        url = f"{LntuTeacherClient.BASE_URL}{LntuTeacherClient.SEARCH_PATH}"
        headers = {"User-Agent": "Mozilla/5.0"}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, params=params) as resp:
                html = await resp.text()

        soup = BeautifulSoup(html, "html.parser")
        teachers: List[Dict[str, str]] = []

        # Для кожного <h3 class="js-views-accordion-group-header"> (літера) беремо
        # усі сусідні <div> (поки не натрапимо на наступний <h3>).
        for group in soup.find_all("h3", class_="js-views-accordion-group-header"):
            letter = group.get_text(strip=True)

            # Ітеруємо всі наступні siblings до наступного <h3>
            for sibling in group.next_siblings:
                if getattr(sibling, "name", None) == "h3":
                    break
                if getattr(sibling, "name", None) != "div":
                    continue

                entry_div = sibling
                a_tag = entry_div.find("a")
                img_tag = entry_div.find("img")
                if not a_tag:
                    continue

                name = a_tag.contents[0].strip()
                title = ""
                if (p := a_tag.find("p")):
                    title = p.get_text(strip=True)

                rel_url = a_tag.get("href", "").strip()
                full_url = LntuTeacherClient.BASE_URL + rel_url

                photo_src = ""
                if img_tag and img_tag.get("src"):
                    src = img_tag["src"].strip()
                    photo_src = (
                        LntuTeacherClient.BASE_URL + src
                        if src.startswith("/")
                        else src
                    )

                teachers.append({
                    "name": name,
                    "title": title,
                    "url": full_url,
                    "photo": photo_src,
                    "letter": letter
                })

        return teachers

    @staticmethod
    async def get_teacher_details(url: str) -> Dict[str, str]:
        """
        Повертає основну інформацію про викладача зі сторінки його профілю.
        URL має вигляд: https://rating2.lntu.edu.ua/uk/{slug}
        """
        headers = {"User-Agent": "Mozilla/5.0"}
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url) as resp:
                html = await resp.text()

        soup = BeautifulSoup(html, "html.parser")

        # Ім'я викладача
        name_block = soup.select_one(".info-bl-pip")
        name = name_block.get_text(strip=True) if name_block else ""

        # Факультет та посада (основне місце роботи)
        faculty = ""
        position = ""
        base_info = soup.select_one(
            ".views-field-field-fakultet-kafedra-osnova .info-bl"
        )
        if base_info:
            lines = base_info.find_all("div")
            # Зазвичай: [порожній <div> для заголовка, факультет, кафедра, посада]
            if len(lines) >= 2:
                faculty = lines[1].get_text(strip=True)
            if len(lines) >= 3:
                position = lines[2].get_text(strip=True)

        # Електронна пошта
        email_tag = soup.select_one(".mail-profile-user a")
        email = email_tag.get_text(strip=True) if email_tag else ""

        # Наукові інтереси
        interests_block = soup.select_one(
            "#edit-group-naukovi-interesi--content .field--item"
        )
        interests = interests_block.get_text(strip=True) if interests_block else ""

        bio_block = soup.select_one(
            "#edit-group-biografiya--content .field--item"
        )
        biography = bio_block.get_text(strip=True) if bio_block else ""

        return {
            "name": name,
            "faculty": faculty,
            "position": position,
            "email": email,
            "interests": interests,
            "biography": biography
        }
