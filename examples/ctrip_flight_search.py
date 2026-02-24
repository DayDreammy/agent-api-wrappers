import asyncio
import sys
sys.path.insert(0, '/home/node/.openclaw/workspace/agent-api-wrappers')

from providers.ctrip import CtripProvider


async def search_flights_example():
    """
    示例：搜索上海到北京的航班
    
    运行方式:
        python examples/ctrip_flight_search.py
    """
    print("🔍 正在搜索航班...")
    print("-" * 50)
    
    async with CtripProvider() as provider:
        # 检查服务状态
        is_healthy = await provider.health_check()
        print(f"✅ 携程网站可访问: {is_healthy}")
        print()
        
        # 搜索航班
        flights = await provider.search_flights(
            origin="SHA",           # 上海虹桥
            destination="PEK",      # 北京首都
            date="2026-03-15"       # 出发日期
        )
        
        print(f"找到 {len(flights)} 个航班:\n")
        
        # 显示前10个结果
        for i, flight in enumerate(flights[:10], 1):
            print(f"{i}. {flight['airline']} {flight['flight_no']}")
            print(f"   出发: {flight['dep_time']} {flight['dep_airport']}")
            print(f"   到达: {flight['arr_time']} {flight['arr_airport']}")
            print(f"   价格: ¥{flight['price']}")
            print(f"   时长: {flight['duration']}")
            print()


if __name__ == "__main__":
    try:
        asyncio.run(search_flights_example())
    except KeyboardInterrupt:
        print("\n\n用户取消")
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
