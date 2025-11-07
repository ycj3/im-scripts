import requests
import time
import json
import statistics # 用于计算平均值等统计数据
import sys

def test_request_latency(url, num_requests=10, timeout=10):
    """
    测试指定 URL 的请求耗时。

    Args:
        url (str): 要测试的 URL。
        num_requests (int): 发送请求的次数。
        timeout (int): 每个请求的超时时间（秒）。
    """
    print(f"开始测试 URL: {url}")
    print(f"请求次数: {num_requests}")
    print(f"请求超时: {timeout} 秒\n")

    latencies = []
    successful_requests = 0
    failed_requests = 0
    _request = requests.Session()
    _request.headers.update({'Authorization': 'Bearer YWMtiC4BNrsPEfCiBDe4rlN3ufx7SXm8kjunk46c47t-jxqlGOLAvekR5oGYWySWBoauAgMAAAGaWTpIagAPoAAIub9AhLKbhaOpI8LCemzPvzUmfKlMF3wVlShXdBySog', 'Content-Type': 'application/json'})

    for i in range(1, num_requests + 1):
        try:
            # 发送 GET 请求，并记录开始时间
            # requests 库的 response.elapsed 属性更精确地表示从发送请求到接收到所有响应数据的时间
            payload = {"from": "demo_user_1","to": ["205815834279941"],"type": "txt","need_group_ack": False,"body": {"msg": "testmessages"}, "ext": {"device_ts": int(time.time() * 1000)}}
            response = _request.post(url, data=json.dumps(payload), timeout=timeout)

            # 检查 HTTP 状态码，如果不是 2xx，则抛出 HTTPError
            response.raise_for_status()

            latency = response.elapsed.total_seconds()
            latencies.append(latency)
            successful_requests += 1
            print(f"请求 {i}/{num_requests}: 成功! 耗时 {latency:.4f} 秒 (状态码: {response.status_code})")

        except requests.exceptions.Timeout:
            failed_requests += 1
            print(f"请求 {i}/{num_requests}: 失败! 超时 ({timeout} 秒)")
        except requests.exceptions.ConnectionError as e:
            failed_requests += 1
            print(f"请求 {i}/{num_requests}: 失败! 连接错误: {e}")
        except requests.exceptions.HTTPError as e:
            failed_requests += 1
            print(f"请求 {i}/{num_requests}: 失败! HTTP 错误: {e} (状态码: {response.status_code})")
        except requests.exceptions.RequestException as e:
            failed_requests += 1
            print(f"请求 {i}/{num_requests}: 失败! 发生未知请求错误: {e}")
        except Exception as e:
            failed_requests += 1
            print(f"请求 {i}/{num_requests}: 失败! 发生意外错误: {e}")

        # 每次请求之间稍作停顿，避免对服务器造成过大压力
        time.sleep(0.1)

    print("\n--- 测试结果总结 ---")
    print(f"总请求次数: {num_requests}")
    print(f"成功请求次数: {successful_requests}")
    print(f"失败请求次数: {failed_requests}")

    if latencies:
        min_latency = min(latencies)
        max_latency = max(latencies)
        avg_latency = statistics.mean(latencies)

        print(f"最小耗时: {min_latency:.4f} 秒")
        print(f"最大耗时: {max_latency:.4f} 秒")
        print(f"平均耗时: {avg_latency:.4f} 秒")

        # 如果需要，可以计算标准差来衡量波动性
        if len(latencies) > 1:
            stdev_latency = statistics.stdev(latencies)
            print(f"耗时标准差: {stdev_latency:.4f} 秒")
    else:
        print("没有成功的请求，无法计算耗时统计数据。")

if __name__ == "__main__":
    target_url = "https://a1.easemob.com/huanxin-test-syq/wkbj/messages/chatgroups"

    # 可以通过命令行参数设置请求次数和超时时间
    # 例如：python test_latency.py 20 5
    if len(sys.argv) > 1:
        try:
            num_req = int(sys.argv[1])
        except ValueError:
            print("错误: 请求次数必须是整数。使用默认值 10。")
            num_req = 10
    else:
        num_req = 10 # 默认请求次数

    if len(sys.argv) > 2:
        try:
            req_timeout = int(sys.argv[2])
        except ValueError:
            print("错误: 超时时间必须是整数。使用默认值 10。")
            req_timeout = 10
    else:
        req_timeout = 10 # 默认超时时间

    test_request_latency(target_url, num_requests=num_req, timeout=req_timeout)