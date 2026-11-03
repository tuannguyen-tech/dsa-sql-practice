"""
==============================================================================
Problem: Merge Sorted Array
Link: https://leetcode.com/problems/merge-sorted-array/description/?envType=problem-list-v2&envId=two-pointers
Difficulty: Easy
Topic: Array
==============================================================================
[1] Cách chạy thuật toán(mô tả trực quan)
vì mỗi mảng đã được sắp xếp và trong mảng nums1 ta còn thừa khoảng trống đằng sau vì vậy tôi nghĩ mình phải tận dụng chúng và tôi sẽ ghi kết quả từ cuối về đầu đều này giúp tôi tránh việc ghi đè lên dữ liệu thật chưa xử lý 
bài toán cho 2 dãy số đã sắp xếp vì vậy tôi nghĩ  nếu tìm số lớn nhất của 2 mảng lần  lượt và đặt vào cuối thì chắc chắn số đó sẽ được sắp xếp

vd: nums1 =[1,2,3,0,0,0], m=3 và nums2=[2,5,6], n=3
tôi sẽ dùng 3 con trỏ:
    + i trỏ đến phần tử thật cuối trong mảng nums1
    + j trỏ đến phần tử cuối cùng  trong mảng nums2
    + k vị trí trống cuối cùng tôi cần ghi trong nums1

[1,2,3,0,0,0]
     i     k
[2,5,6]
     j 
B1: nums1[i] = 3 vs nums2[j] = 6  6>3
    -> nums1[k] =6; j--; k--
    nums1: [1,2,3,0,0,6]
[1,2,3,0,0,6]
     i   k
[2,5,6]
   j

B2: nums1[i] =3 và nums2[j]=5  5>3
    -> nums1[k] = 5; j--; k--
    nums1: [1,2,3,0,5,6]
[1,2,3,0,5,6]
     i k
[2,5,6]
 j

B3: nums1[i] =3 và nums2[j]=2 3>2
    -> nums1[k] =3; i--; k--
    nums1: [1,2,3,3,5,6]
[1,2,3,3,5,6]
   i k
[2,5,6]

B4 nums1[i]=2 và nums2[j] =2 ->bằng nhau
   -> nums1[k] =2; j--; k--
   nums1: [1,2,2,3,5,6]

Lúc này j=-1 ta dừng vòng lặp

Kết quả: nums1 =[1,2,2,3,5,6]

[2] Các bước thuật toán
B1. Khởi tạo 3 con trỏ:
        i <- m-1 (trỏ đến cuối phần dữ liệu thật cuae nums1)
        j <- n-1 (cuối nums2)
        k <- m + n -1 (ô trống cuối cùng của nums1)
B2. Lặp while j>=0:
      Nếu i>=0 và nums1[i] >nums2[j]:
        nums1[k] <- nums1[i]
        i <- i-1
      Ngược lại: (khi i<0 hoặc nums1[i] <=nums2[j]):
        nums1[k] <- nums2[j]
        j <- j-1
      k <- k-1

-Tại sao khi so sánh nums1[i] với nums2[j] ta phải kiểm tra i>=0 trước?
(Bởi vì nếu i giảm xuống -1 trong python nó sẽ trỏ đến phần tử cuối mảng vì vậy sẽ làm kết quả sai)
-Tại sao ta lại phải chạy đến khi j<=0?
vì có một trường hợp
[7,8,9,0,0,0]
     i k
[1,2,3]
     j
nếu theo thuật toán thì kết quả sẽ là:
    [7,8,9,7,8,9]
  i      k
     [1,2,3]
          j
Lúc này i đã chạy hết nhưng các phần tử trong nums2 vẫn không được thêm vô mảng nums1
Lúc đó ta sẽ đổ các phần tử còn lại trong nums2  vào nums1  đến khi j >=0 từ k vị trí còn lại


[3] complexity 
-Time complexity: O(N) - Vì mỗi phần tử trong mảng nums1 và nums2 chỉ được xét tối đa 1 lần
-Space Complexuty:O(1) - Vì chỉ dùng 3 biến con trỏ i,j,k, không tạo mảng phụ.
==============================================================================
"""

def merge(num1,m,num2,n):
    i = m -1
    j = n-1
    k = m+n-1

    while j>=0:
        if i>=0 and num1[i] > num2[j]:
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


