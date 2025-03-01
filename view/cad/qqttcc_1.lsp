(defun c:qttcc (/ ss i ent entType delCount)
  ;; 初始化删除计数器
  (setq delCount 0)

  ;; 提示用户选择对象
  (if (setq ss (ssget '((0 . "HATCH")))) ;; 过滤仅获取填充对象
    (progn
      ;; 遍历所选的对象集合
      (setq i 0)
      (repeat (sslength ss)
        (setq ent (ssname ss i)) ;; 获取实体名
        (setq entType (cdr (assoc 0 (entget ent)))) ;; 获取实体类型

        ;; 如果是填充实体，则删除之
        (if (or (equal entType "HATCH") ;; 普通填充
                (equal entType "AHATCH")) ;; 关联填充，如果有的话
          (progn
            (vla-delete (vlax-ename->vla-object ent)) ;; 删除实体
            (setq delCount (+ delCount 1)) ;; 计数器加一
          )
        )
        (setq i (+ i 1))
      )

      ;; 显示操作结果
      (if (> delCount 0)
        (prompt (strcat "\n成功删除了 " (itoa delCount) " 个填充对象。"))
        (prompt "\n没有找到可以删除的填充对象。")
      )
    )
    ;; 如果用户没有选择任何对象
    (prompt "\n未选择任何填充对象。")
  )
  (princ) ;; 清除命令行
)

(princ "\n加载成功：输入 'qttcc' 命令以执行批量删除填充对象。\n")