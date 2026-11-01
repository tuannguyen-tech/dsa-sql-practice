"""
==============================================================================
Problem: Merge Sorted Array
Link: https://leetcode.com/problems/merge-sorted-array/description/?envType=problem-list-v2&envId=two-pointers
Difficulty: Easy
Topic: Array
==============================================================================
[1] approach
vì mỗi mảng đã được sắp xếp và trong mảng nums1 ta còn thừa khoảng trống đằng sau vì vậy tôi nghĩ mình phải tận dụng chúng
bài toán cho 2 dãy số đã sắp xếp vì vậy tôi nghĩ  nếu tìm số lớn nhất của 2 mảng lần  lượt và đặt vào cuối thì chắc chắn số đó dẽ được sắp xếp

vd: nums1 =[1,2,3,0,0,0] và nums2=[2,5,6]
tôi sẽ dùng 3 con trỏ:
    + i đánh dấu số lớn nhất trong mảng nums1
    + j đánh dấu số lớn nhất trong mảng nums2
    + k vị trí tôi ghi phần tử được chọn từ cuối mảng nums1 đổ lại

[1,2,3,0,0,0]
     i     k 
[2,5,6]
      j
đầu tiên nums1[i] <nums2[j] => nums[k] = nums2[j]
(sau đó  giảm k một đơn vị giảm j một đơn vị) (giảm j bởi vì ta đang cố gắng ghi j vào mảng nums1)

[1,2,3,0,0,6]
     i   k
[2,5,6]
   j
num1[i] <nums2[j] làm tương tự bước trước

[1,2,3,0,5,6]
     i k
[2,5,6]
 j

lúc này nums1[i] > nums2[j] =>nums[k] = nums1[k] = nums1[i]
(và lúc này giảm i  và  k) đến khi nào nums1[i] <= nums2[j](bởi vì có thể có các số khác về trước  lớn hơn nums1[j] vì vậy ta sẽ cần điều chỉnh lại thứ tự bằng cách ghi đè tiếp vào vị trí k)
[1,2,3,3,5,6]
   i k
[2,5,6]
 j

tại đây nums1[i] <= nums2[j] 

[1,2,2,3,5,6]
   i
   k
lúc này j đã chạy hết
và ta được mảng nums1 như sau: [1,2,2,3,5,6]

[2] complexity 
-Time complexity: O(N) - Vì chỉ duyệt mảng một lần
-Space Complexuty:O(1) -Vì không chiếm thêm bất kỳ bộ nhớ nào
==============================================================================
"""

def merge(num1,m,num2,n):
    i = m -1
    j = n-1
    k = m+n-1

    while j>=0:
        if num1[i] > num2[j] and i>=0:
            num1[k] = num1[i]
            i-=1
        else:
            num1[k] = num2[j]
            j-=1

        k-=1

    return num1
# ---test cases ---
if __name__ == '__main__':
    print(merge([1,2,3,0,0,0],3,[2,5,6],3))


