import requests
import time
import wave
import io


def pcm2wav(pcm_data):
    with wave.open('./outputs/index_tts_streaming_output2.wav', "wb") as wav:
        wav.setnchannels(1)  # 设置声道数
        wav.setsampwidth(2)  # 设置采样宽度
        wav.setframerate(24000)  # 设置采样率
        wav.writeframes(pcm_data)  # 写入 PCM 数据


import pyaudio

p = pyaudio.PyAudio()
audio_format = pyaudio.paInt16  # Assuming 16-bit PCM format

# 可通过输出设备播放音频
# stream = p.open(
#     format=audio_format, channels=1, rate=24000, output=True
# )

wf = wave.open(f"./outputs/index_tts_streaming_output.wav", "wb")
wf.setnchannels(1)
wf.setsampwidth(p.get_sample_size(audio_format))
wf.setframerate(24000)

stream_stopped_flag = False


def test_tts_streaming():
    """测试流式 TTS"""
    print("测试流式 TTS...")

    # data = {
    #     # "text": """在新车预告一个月后，特斯拉大六座MODEL Y L正式上市。8月19日，特斯拉中国官网上线Model Y L车型，33.9万元起售，预计交付时间2025年9月。据官方介绍，Model Y L上市的同时，还推出了“首付99900元起，享3年0息”和“首付45900元起，享5年超低息”的金融福利，叠加8000元车漆选装礼金和三种特享充电权益，Model Y L车主在新车上市之初就能享受到价值约3万元的购车福利。Model Y L是一款大六座豪华纯电SUV，车身加长179mm，轴距加长150mm，储物空间达到2539升。全车座椅进行了重新设计，前排座椅新增可调头枕与腿托；二排采用独立座椅，可进行多向电动调节；三排座椅也具备i-Size儿童安全座椅接口，并可进行靠背角度的电动调节。全车前排、二排座椅具备加热与通风功能，三排座椅具备加热功能。""",
    #     "text":"红色安全帽（顶部有黑色摄像头模块，无LOGO）；白色工程安全帽（顶部印有“华微软件”及英文“HUAWEISOFT”标志）",
    #     "reference_id": "broadcast",
    #     "streaming": True,
    #     # "speed": 1.0,
    #     # "mode": "zero_shot",
    #     # "format": "wav"
    # }
    data = {
        # "text": """在新车预告一个月后，特斯拉大六座MODEL Y L正式上市。8月19日，特斯拉中国官网上线Model Y L车型，33.9万元起售，预计交付时间2025年9月。据官方介绍，Model Y L上市的同时，还推出了“首付99900元起，享3年0息”和“首付45900元起，享5年超低息”的金融福利，叠加8000元车漆选装礼金和三种特享充电权益，Model Y L车主在新车上市之初就能享受到价值约3万元的购车福利。Model Y L是一款大六座豪华纯电SUV，车身加长179mm，轴距加长150mm，储物空间达到2539升。全车座椅进行了重新设计，前排座椅新增可调头枕与腿托；二排采用独立座椅，可进行多向电动调节；三排座椅也具备i-Size儿童安全座椅接口，并可进行靠背角度的电动调节。全车前排、二排座椅具备加热与通风功能，三排座椅具备加热功能。""",
        "text":"红色安全帽（顶部有黑色摄像头模块，无LOGO）；白色工程安全帽（顶部印有“华微软件”及英文“HUAWEISOFT”标志）",
        "reference_id": "broadcast",
        "streaming": True,
        # "speed": 1.0,
        # "mode": "zero_shot",
        # "format": "wav"
    }
    st = time.time()
    try:
        response = requests.post("http://192.168.0.18:11996/index-tts/v1/tts_stream", json=data, stream=True)
        print(f"请求耗时：{time.time() - st:.2f}s")

        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")

        if response.status_code == 200:
            if data['streaming']:
                audio_content = b''
                for chunk in response.iter_content(chunk_size=24000):  # 使用16000作为chunk_size,与音频采样率匹配,可以更好地处理音频数据
                    et=time.time()
                    print("耗时：",et-st)
                    audio_content += chunk
                    if chunk:
                        # stream.write(chunk)
                        wf.writeframesraw(chunk)
                    else:
                        if not stream_stopped_flag:
                            # stream.stop_stream()
                            stream_stopped_flag = True
                print(f"流式音频已保存为 index_tts_streaming_output.wav，大小: {len(audio_content)} bytes")
            else:
                audio_content = response.content
                pcm2wav(audio_content)
                print(f"流式音频已保存为 index_tts_streaming_output2.wav，大小: {len(audio_content)} bytes")
        else:
            print(f"错误响应: {response.text}")

    except Exception as e:
        print(f"流式 TTS 测试失败: {e}")
    finally:
        # stream.close()
        p.terminate()
        wf.close()


def test_tts_non_streaming():
    """测试非流式 TTS"""
    print("\n测试非流式 TTS...")

    data = {
        "text": "红色安全帽（顶部有黑色摄像头模块，无LOGO）；白色工程安全帽（顶部印有“华微软件”及英文“HUAWEISOFT”标志）",
        "reference_id": "broadcast"
    }

    st = time.time()
    try:
        response = requests.post("http://192.168.0.18:11996/index-tts/v1/tts", json=data, stream=False)
        print(f"请求耗时：{time.time() - st:.2f}s")
        print(f"状态码: {response.status_code}")
        print(f"响应头: {dict(response.headers)}")

        if response.status_code == 200:
            audio_content = response.content

            # 保存音频文件
            with open('./outputs/index_tts_non_streaming_output.wav', 'wb') as f:
                f.write(audio_content)
            print(f"非流式音频已保存为 index_tts_non_streaming_output.wav，大小: {len(audio_content)} bytes")
        else:
            print(f"错误响应: {response.text}")

    except Exception as e:
        print(f"非流式 TTS 测试失败: {e}")


if __name__ == '__main__':
    print("开始测试修改后的 TTS 服务...")
    print("=" * 50)

    test_tts_streaming()
    # test_tts_non_streaming()

    print("\n" + "=" * 50)
    print("测试完成！")
