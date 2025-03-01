import win32com.client
from pyautocad import Autocad, APoint


def main():
    try:
        # 连接到AutoCAD应用程序
        acad = Autocad(create_if_not_exists=True)

        # 提示用户选择对象
        acad.prompt("请框选或点选需要处理的对象。\n")
        # 创建临时选择集并让用户在屏幕上选择对象
        selection = acad.doc.SelectionSets.Add("TempSelectionSet")
        selection.SelectOnScreen()

        # 初始化填充对象计数器
        fill_count = 0

        # 遍历选择集中的对象
        for entity in selection:
            # 检查对象是否为填充对象
            if entity.EntityName == 'AcDbHatch':
                # 删除填充对象
                entity.Delete()
                fill_count += 1

        # 删除临时选择集
        selection.Delete()

        # 操作反馈
        if fill_count > 0:
            acad.prompt(f"已成功删除 {fill_count} 个填充对象。\n")
        else:
            acad.prompt("未找到填充对象。\n")

        # 绘制半径为5m的圆
        center_point = APoint(0, 0)  # 可根据需要修改圆心坐标
        radius = 5
        acad.doc.ModelSpace.AddCircle(center_point, radius)

    except Exception as e:
        print(f"发生错误：{e}")


if __name__ == "__main__":
    main()
