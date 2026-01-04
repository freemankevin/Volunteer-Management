#!/usr/bin/env python3
"""
测试运行脚本
运行所有单元测试，跳过需要真实API的集成测试
"""
import sys
import os
import subprocess

def run_unit_tests():
    """运行单元测试"""
    print("🧪 开始运行单元测试...")
    
    # 运行模型测试
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/test_volunteer.py",
        "tests/test_event.py", 
        "tests/test_schedule.py",
        "-v",
        "--tb=short"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(os.path.abspath(__file__)))
        print("STDOUT:")
        print(result.stdout)
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ 所有单元测试通过！")
        else:
            print(f"❌ 单元测试失败，返回码: {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 运行测试时出错: {e}")
        return False

def run_all_tests():
    """运行所有测试"""
    print("🚀 开始运行所有测试...")
    
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short"
    ]
    
    try:
        result = subprocess.run(cmd, cwd=os.path.dirname(os.path.abspath(__file__)))
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ 运行测试时出错: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--all":
        success = run_all_tests()
    else:
        success = run_unit_tests()
    
    sys.exit(0 if success else 1)