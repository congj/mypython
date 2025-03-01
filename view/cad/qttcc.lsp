(defun rand (low high)
  "Generate a random number between low and high."
  ;; 使用当前日期时间作为种子值，保证每次启动时产生不同的序列
  (setq seed (getvar "DATE"))
  ;; 缩小种子范围并利用绘图中的时间差进一步打乱种子
  (setq seed (rem seed 1000000))
  (setq seed (fix (* seed (getvar "TDINDWG"))))
  ;; 取绝对值避免负数，并计算范围内随机数
  (setq seed (abs seed))
  (+ low (rem seed (- high low 1)))
)

(defun c:drawRandomCircles (/ i radius x y)
  ;; 初始化随机数生成器
  (setq seed (getvar "DATE"))
  
  ;; 开始一个事务以优化性能
  (vla-startundomark (vla-get-activedocument (vlax-get-acad-object)))
  
  (setq i 0)
  ;; 绘制20个圆
  (while (< i 20)
    ;; 圆的半径在1到5之间随机
    (setq radius (rand 1 5))
    ;; 圆心x坐标在-100到100之间随机
    (setq x (rand -100 100))
    ;; 圆心y坐标在-100到100之间随机
    (setq y (rand -100 100))
    ;; 在指定位置和尺寸绘制圆
    (command "_.circle" (list x y 0) radius)
    ;; 计数器加一
    (setq i (+ i 1))
  )
  
  ;; 结束事务
  (vla-endundomark (vla-get-activedocument (vlax-get-acad-object)))
  
  (princ)
)

(princ "\n加载成功：输入 'drawRandomCircles' 来随机绘制多个圆。\n")