import json
import aiohttp
from dto import AbstractDto
from dto import vnz_osvita


class VnzOsvitaApi:
    BASE_URL = "https://vnz.osvita.net/WidgetSchedule.asmx"

    @staticmethod
    async def _get(endpoint: str, dto: AbstractDto) -> dict:
        params = dto.to_payload()
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Accept": "*/*",
            "Referer": "https://vnz.osvita.net/",
            "Origin": "https://vnz.osvita.net",
        }
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{VnzOsvitaApi.BASE_URL}/{endpoint}", params=params, headers=headers) as resp:
                text = await resp.text()
                print(resp)
                if resp.status != 200:
                    return {"error": f"HTTP {resp.status}", "raw": text}

                try:
                    json_str = text[text.find("(") + 1:text.rfind(")")]
                    response = json.loads(json_str)
                    return response.get('d')
                except Exception:
                    return {"error": "Invalid response", "raw": text}

    @staticmethod
    async def get_faculties(dto: vnz_osvita.GetFacultiesDto) -> dict:
        return await VnzOsvitaApi._get("GetStudentScheduleFiltersData", dto)

    @staticmethod
    async def get_study_groups(dto: vnz_osvita.GetStudyGroupsDto) -> dict:
        return await VnzOsvitaApi._get("GetStudyGroups", dto)

    @staticmethod
    async def get_schedule(dto: vnz_osvita.GetScheduleDto) -> dict:
        return await VnzOsvitaApi._get("GetScheduleDataX", dto)
