from loguru import logger
from sys import stdout
from mitmproxy import http, ctx
import json
# You should not modify the following variables
userInfo = {
    "nickname": "Default",
    "userID": 123456789,
}
roleInfo = {
    "roleID": 10018,
    "skinID": 1001801,
}

logger.remove()
logger.add(stdout, colorize=True,
        format='<cyan>[{time:HH:mm:ss.SSS}]</cyan> <level>{message}</level>')

class WebSocketAddon:
    def websocket_message(self, flow: http.HTTPFlow):
        global userInfo, roleInfo
        assert flow.websocket is not None  # make type checker happy
        message = flow.websocket.messages[-1]
        data = message.content
        if not message.injected:
            # 找到 JSON 数据的起始位置
            json_start = data.find(b'{')
            if json_start != -1:
                json_data = data[json_start:].decode('utf-8')
                # 解析 JSON 数据
                parsed_data = json.loads(json_data)
                # 修改指定玩家的 role_id
                if "cmd" in parsed_data and parsed_data["cmd"] == "cmd_enter_room":
                    for player in parsed_data['data']['players']:
                        if player['user']['user_id'] == userInfo['userID']:
                            player['user']['role_id'] = roleInfo['roleID']
                            player['user']['skin_id'] = roleInfo['skinID']
                            # 将修改后的数据编码回 JSON 字符串
                            modified_json_data = json.dumps(parsed_data,ensure_ascii=False)
                            cleaned_json_data = modified_json_data.replace(', ', ',').replace(': ', ':')
                            newLen = len(cleaned_json_data.encode('utf-8')) + 15
                            newLenHex = newLen.to_bytes(2, byteorder='big')
                            newData = data[:json_start][:2] + newLenHex + data[:json_start][4:]
                            # 重新编码为 bytes 数据
                            modified_data = newData + cleaned_json_data.encode('utf-8')
                            message.drop()
                            ctx.master.commands.call(
                            "inject.websocket", flow, True, modified_data, False)
addons = [
    WebSocketAddon()
]
def response(flow: http.HTTPFlow) -> None:
    global userInfo, roleInfo
    if "/users/emailLogin" in flow.request.path:
        if flow.response.content:
            try:
                response_data = json.loads(flow.response.content)
                userInfo['userID'] = response_data['data']['user']['id']
                userInfo['nickname'] = response_data['data']['user']['nickname']
                logger.info(f"User {userInfo['nickname']} logged in")
                logger.info(f"User ID: {userInfo['userID']}")
            except json.JSONDecodeError:
                pass
    if "/users/tokenLogin" in flow.request.path:
        if flow.response.content:
            try:
                logger.debug("Modifying response for /users/tokenLogin")
                response_data = json.loads(flow.response.content)
                logger.debug(f"Request data: {response_data}")
                userInfo['userID'] = response_data['data']['user']['id']
                userInfo['nickname'] = response_data['data']['user']['nickname']
                logger.info(f"User {userInfo['nickname']} logged in")
                logger.info(f"User ID: {userInfo['userID']}")
            except json.JSONDecodeError:
                pass
    # 如果 URL 的后半部分包含 /users/getSkinInfo
    if "/users/getSkinInfo" in flow.request.path:
        # 修改响应体
        if flow.response.content:
            try:
                response_data = json.loads(flow.response.content)
                # 将每个属性的 isOwn 修改为 True
                for item in response_data.get('data', []):
                    item['isOwn'] = True
                # 更新响应体
                flow.response.content = json.dumps(response_data, ensure_ascii=False).encode('utf-8')
            except json.JSONDecodeError:
                pass  # 忽略无法解析的响应体
    
    # 如果 URL 的后半部分包含 /users/updateRoleInfo
    elif "/users/updateRoleInfo" in flow.request.path:
        request_data = json.loads(flow.request.content)
        roleInfo['roleID'] = request_data['roleID']
        logger.info(f"Role ID: {roleInfo['roleID']}")
        roleInfo['skinID'] = request_data['skinID']
        logger.info(f"Skin ID: {roleInfo['skinID']}")

        # 返回固定的 JSON 响应
        response_data = {
            "code": 0,
            "data": True,
            "message": "ok"
        }
        flow.response.content = json.dumps(response_data, ensure_ascii=False).encode('utf-8')
        flow.response.headers["Content-Type"] = "application/json"
    
    # 如果 URL 的后半部分包含 /users/getRoleInfo
    elif "/users/getRoleInfo" in flow.request.path:
        # 修改响应体
        if flow.response.content:
            try:
                response_data = json.loads(flow.response.content)
                # 将 roleList 中的 isOwn 修改为 True
                for role in response_data.get('data', {}).get('roleList', []):
                    role['isOwn'] = True
                # 更新响应体
                response_data['data']['useRoleID'] = roleInfo['roleID']
                response_data['data']['useSkinID'] = roleInfo['skinID']
                flow.response.content = json.dumps(response_data, ensure_ascii=False).encode('utf-8')
            except json.JSONDecodeError:
                pass  # 忽略无法解析的响应体
    elif "/lobbys/" in flow.request.path:
        # 检查响应内容
        if flow.response.content:
            try:
                response_data = json.loads(flow.response.content)
                logger.debug(f"Request data: {response_data}")
                logger.debug(f"Type of request data: {type(response_data)}")
                # 修改响应数据中的 roleId
                for player in response_data['data']['players']:
                    if player['userID'] == userInfo['userID']:
                        logger.debug(f"Found player data: {player}")
                        player['roleId'] = roleInfo['roleID']
                        player['skinID'] = roleInfo['skinID']
                # 更新响应体
                flow.response.content = json.dumps(response_data, ensure_ascii=False).encode('utf-8')
            except json.JSONDecodeError:
                pass  # 忽略无法解析的响应体
    elif "/users/homeUserData" in flow.request.path:
        # 检查响应内容
        if flow.response.content:
            try:
                response_data = json.loads(flow.response.content)
                response_data['data']['roleID'] = roleInfo['roleID']
                response_data['data']['skinID'] = roleInfo['skinID']
                # 更新响应体
                flow.response.content = json.dumps(response_data, ensure_ascii=False).encode('utf-8')
            except json.JSONDecodeError:
                pass  # 忽略无法解析的响应体
    elif "/users/userBaseData" in flow.request.path:
        # 检查响应内容
        if flow.response.content:
            try:
                response_data = json.loads(flow.response.content)
                response_data['data']['roleID'] = roleInfo['roleID']
                response_data['data']['skinID'] = roleInfo['skinID']
                # 更新响应体
                flow.response.content = json.dumps(response_data, ensure_ascii=False).encode('utf-8')
            except json.JSONDecodeError:
                pass  # 忽略无法解析的响应体