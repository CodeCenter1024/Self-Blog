## 快速排序算法实现

**日期：2024年5月20日**  •  #算法 #Python

```python
def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr)//2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

print(quick_sort([3,6,8,10,1,2,1]))
```

### 算法复杂度分析
- 时间复杂度：平均O(n log n)
- 空间复杂度：O(log n)

### 应用场景
1. 大数据量排序
2. 需要不稳定排序的场景
3. 内存受限环境