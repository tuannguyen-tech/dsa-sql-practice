# Squares of a Sorted Array

[LeetCode problem](https://leetcode.com/problems/squares-of-a-sorted-array/description/) | **Difficulty:** Easy  
**Topics:** Array, Two Pointers, Sorting

## Solution

Xem lời giải Python tại [`solution.py`](solution.py).

<details>
<summary>Giải thích chi tiết</summary>

## Cách chạy thuật toán (mô tả trực quan)
Ý tưởng: Mảng đã sắp xếp tăng dần, nhưng bình phương lên thì KHÔNG còn tăng
nữa — vì số âm lớn (đầu mảng) bình phương thành số dương lớn. Kết quả có
dạng "chữ V": lớn ở hai đầu, nhỏ ở giữa. Ta lấp đầy mảng kết quả từ CUỐI
về ĐẦU, mỗi lần chọn giá trị tuyệt đối LỚN HƠN trong hai đầu.

Ẩn dụ: Hai đầu của một sợi dây cao su bị kéo căng. Bạn muốn cắt sợi dây
thành từng đoạn và xếp từ đoạn DÀI NHẤT xuống đoạn NGẮN NHẤT. Mỗi lần bạn
so sánh hai đầu sợi dây (trái và phải), đầu nào "xa tâm" hơn (trị tuyệt
đối lớn hơn) thì cắt ra trước — vì nó chắc chắn là đoạn dài nhất còn lại.

Vì sao không sort lại sau khi bình phương?
    Bình phương xong rồi sort là O(n log n) — chậm hơn O(n) mà đề Follow-up
    yêu cầu. Với n = 10^4, O(n log n) ~ 10^4 * 14 = 140.000 phép so sánh,
    còn O(n) chỉ 10.000. Chênh 14 lần. Đề gợi ý "tận dụng mảng đã sort sẵn".

Vì sao phải điền từ CUỐI mảng kết quả về ĐẦU?
    Vì ta luôn chọn được giá trị LỚN NHẤT trong các giá trị còn lại (nhờ so
    sánh hai đầu). Giá trị lớn nhất phải nằm ở CUỐI mảng kết quả (tăng dần).
    Nếu điền từ đầu, ta sẽ cần biết giá trị NHỎ NHẤT trước — mà giá trị nhỏ
    nhất lại nằm ở GIỮA mảng gốc (sau khi bình phương), không dễ lấy.

Vì sao so sánh abs() mà không so sánh trực tiếp?
    nums = [-4, -1, 0, 3, 10]. Nếu so sánh trực tiếp: -4 < 10 → chọn 10 (đúng),
    nhưng -4 < 3 → chọn 3 (SAI, vì |-4|=4 > |3|=3, phải chọn -4). Số âm luôn
    nhỏ hơn số dương, nên so sánh trực tiếp sẽ LUÔN chọn bên phải → bỏ sót
    toàn bộ số âm lớn. Phải dùng abs() để so sánh "độ lớn thực".

Ví dụ 1: nums = [-4, -1, 0, 3, 10]

    Bước A: res = [0, 0, 0, 0, 0], left = 0, right = 4, index = 4

    Bước B: so sánh |nums[left]| và |nums[right]|
        Lần 1: |-4|=4 vs |10|=10 → 10 lớn hơn → res[4]=100, right=3, index=3
        Lần 2: |-4|=4 vs |3|=3   → 4 lớn hơn  → res[3]=16,  left=1,  index=2
        Lần 3: |-1|=1 vs |3|=3   → 3 lớn hơn  → res[2]=9,   right=2, index=1
        Lần 4: |-1|=1 vs |0|=0   → 1 lớn hơn  → res[1]=1,   left=2,  index=0
        Lần 5: |0|=0  vs |0|=0   → 0 lớn hơn  → res[0]=0,   right=1, index=-1

    Bước C: left=2 > right=1 → dừng. res = [0, 1, 9, 16, 100] ✅

Ví dụ 2: nums = [-7, -3, 2, 3, 11]

    Bước A: res = [0,0,0,0,0], left=0, right=4, index=4

    Bước B:
        Lần 1: |-7|=7 vs |11|=11 → chọn 11 → res[4]=121, right=3
        Lần 2: |-7|=7 vs |3|=3   → chọn -7 → res[3]=49,  left=1
        Lần 3: |-3|=3 vs |3|=3   → chọn 3  → res[2]=9,   right=2
        Lần 4: |-3|=3 vs |2|=2   → chọn -3 → res[1]=9,   left=2
        Lần 5: |2|=2  vs |2|=2   → chọn 2  → res[0]=4,   right=1

    Bước C: left=2 > right=1 → dừng. res = [4, 9, 9, 49, 121] ✅

Ví dụ 3 (mảng toàn âm): nums = [-5, -4, -3]

    Bước A: res=[0,0,0], left=0, right=2, index=2
    Lần 1: |-5|=5 vs |-3|=3 → chọn -5 → res[2]=25, left=1
    Lần 2: |-4|=4 vs |-3|=3 → chọn -4 → res[1]=16, left=2
    Lần 3: |-3|=3 vs |-3|=3 → chọn -3 → res[0]=9,  right=1
    res = [9, 16, 25] ✅  (đúng: bình phương [-5,-4,-3] = [25,16,9], sort = [9,16,25])

Ví dụ 4 (mảng toàn dương): nums = [1, 4, 9]

    Tương tự, luôn chọn bên phải (vì bên phải lớn hơn) → res = [1, 16, 81] ✅


## Các bước thuật toán
B1. Khởi tạo mảng kết quả và hai con trỏ:
        res   <- [0] * len(nums)
        left  <- 0
        right <- len(nums) - 1
        index <- len(nums) - 1        (điền từ cuối về đầu)

B2. Lặp khi left <= right:
        Nếu |nums[left]| > |nums[right]|:
            res[index] <- nums[left] ** 2
            left <- left + 1
        Ngược lại:
            res[index] <- nums[right] ** 2
            right <- right - 1
        index <- index - 1

B3. Trả về res.


>> Tại sao dùng "while left <= right" mà không phải "while left < right"?
    Phải dùng "<=" vì khi left == right (còn 1 phần tử chưa xử lý), ta vẫn
    cần xử lý phần tử đó. Nếu dùng "<", phần tử giữa sẽ bị bỏ sót (với mảng
    lẻ phần tử). Ví dụ nums=[0] → left=0, right=0 → phải vào vòng lặp để
    điền res[0]=0.

>> Tại sao dùng "nums[left] ** 2" mà không phải "nums[left] * nums[left]"?
    Cả hai tương đương về kết quả. "**2" ngắn hơn, rõ ý "bình phương" hơn.
    Hiệu năng: "x*x" nhanh hơn "x**2" một chút (vì **2 gọi hàm pow), nhưng
    với n=10^4 thì chênh lệch không đáng kể. Tùy style, không sai.

>> Tại sao điều kiện là "|left| > |right|" mà không phải ">=" hay "<"?
    - Dùng ">" : khi bằng nhau, chọn bên phải (hoặc bên trái đều đúng, vì
      cùng giá trị bình phương). Chọn bên phải là quy ước phổ biến.
    - Dùng ">=": tương tự, chỉ đổi bên được chọn khi hòa.
    - Dùng "<": ĐẢO ngược logic — sẽ chọn bên phải khi bên phải NHỎ HƠN
      → sai hoàn toàn. Cần cẩn thận với chiều so sánh.

>> Tại sao phải dùng mảng "res" riêng mà không sửa trực tiếp "nums"?
    Vì khi điền từ cuối về đầu, ta có thể ghi đè lên giá trị gốc mà con trỏ
    left/right còn cần dùng. Ví dụ: index == right → ghi res[index] sẽ xóa
    nums[right] trước khi kịp bình phương → so sánh các bước sau bị sai.
    Dùng mảng riêng "res" thì nums gốc luôn nguyên vẹn → an toàn.

>> Tại sao không cần "if left < len(nums)" hay kiểm tra biên nào khác?
    Vì vòng lặp "while left <= right" đảm bảo:
        - left luôn nằm trong [0, len(nums)] (tăng khi chọn trái, tối đa
          bằng right+1).
        - right luôn nằm trong [-1, len(nums)-1] (giảm khi chọn phải, tối
          thiểu bằng left-1).
    Khi left == right == một giá trị hợp lệ → xử lý 1 phần tử cuối.
    Khi left > right → mọi phần tử đã được xử lý → dừng.
    Không có trường hợp truy cập ngoài mảng.


## Tại sao chọn bên nào thì nhích con trỏ bên đó?
Đây là CÂU HỎI CỐT LÕI của mọi thuật toán two-pointer. Có 3 góc nhìn.

--- Góc nhìn 1: "Cái xô nước" — mỗi con trỏ là "cái nắp" ---------------------
    Hãy tưởng tượng mảng nums là một hàng ống nước xếp ngang, mỗi ống chứa
    1 số.
        - left  là "nắp đậy" ở đầu trái — chỉ vào ống NGOÀI CÙNG BÊN TRÁI
          CHƯA LẤY.
        - right là "nắp đậy" ở đầu phải — chỉ vào ống NGOÀI CÙNG BÊN PHẢI
          CHƯA LẤY.

    Mỗi bước, bạn CHỈ ĐƯỢC MỞ 1 NẮP để lấy nước (vì mỗi lần chỉ chọn 1
    phần tử):
        - Nếu mở nắp trái (lấy nums[left]) → ống đó ĐÃ LẤY XONG → nắp trái
          phải DỊCH SANG ỐNG KẾ TIẾP (left += 1), để lần sau không mở lại
          ống đã lấy.
        - Nếu mở nắp phải (lấy nums[right]) → nắp phải DỊCH SANG TRÁI
          (right -= 1).

    Nếu QUÊN dịch nắp: lần sau bạn lại mở đúng ống vừa lấy → LẤY TRÙNG
    phần tử đó → mảng kết quả bị LẶP GIÁ TRỊ và THIẾU phần tử khác.

--- Góc nhìn 2: "Vùng chưa xử lý" — bất biến vòng lặp ----------------------
    Đây là góc nhìn CHẶT CHẼ NHẤT (dùng trong chứng minh thuật toán).

    BẤT BIẾN (invariant) của vòng lặp:
        "Tại mọi thời điểm, đoạn nums[left .. right] chính là VÙNG CHƯA
         ĐƯỢC XỬ LÝ. Mọi phần tử ngoài đoạn này đã được bình phương và
         đặt vào res rồi."

    Kiểm tra:
        | Thời điểm              | Vùng chưa xử lý     | Phần tử đã xử lý         |
        |------------------------|---------------------|--------------------------|
        | Ban đầu                | nums[0 .. n-1]      | không có                 |
        | Sau khi chọn nums[left]| nums[left+1 .. right]| nums[left] đã vào res   |
        | Sau khi chọn nums[right]| nums[left .. right-1]| nums[right] đã vào res  |
        | Kết thúc (left > right)| rỗng                | tất cả                   |

    Vì vậy:
        - Khi chọn TRÁI → phần tử nums[left] RỜI KHỎI vùng chưa xử lý →
          vùng mới bắt đầu từ left+1 → PHẢI left += 1.
        - Khi chọn PHẢI → phần tử nums[right] RỜI KHỎI vùng chưa xử lý →
          vùng mới kết thúc ở right-1 → PHẢI right -= 1.

    Nếu KHÔNG di chuyển con trỏ, vùng chưa xử lý KHÔNG CO LẠI → vòng lặp
    KHÔNG BAO GIỜ KẾT THÚC (hoặc lấy trùng phần tử).

--- Góc nhìn 3: "Tại sao không di chuyển CẢ HAI?" -------------------------
    Bạn có thể thắc mắc: "Sao không left += 1 và right -= 1 cùng lúc?"

    Vì MỖI LẦN CHỈ CHỌN 1 PHẦN TỬ — phần tử có TRỊ TUYỆT ĐỐI LỚN NHẤT
    trong vùng còn lại. Phần tử còn lại (bên kia) CHƯA ĐƯỢC DÙNG, nó vẫn
    nằm trong vùng chưa xử lý, có thể là ỨNG VIÊN CHO LẦN CHỌN SAU.

    Ví dụ cụ thể: nums = [-4, -1, 0, 3, 10]

        | Bước | left | right | Vùng chưa xử lý      | Chọn      | Vì sao?       |
        |------|------|-------|----------------------|-----------|---------------|
        | 1    | 0    | 4     | [-4,-1,0,3,10]       | 10 (phải) | |10| > |-4|   |
        | 2    | 0    | 3     | [-4,-1,0,3]          | -4 (trái) | |-4| > |3|    |
        | 3    | 1    | 3     | [-1,0,3]             | 3 (phải)  | |3| > |-1|    |
        | 4    | 1    | 2     | [-1,0]               | -1 (trái) | |-1| > |0|    |
        | 5    | 2    | 2     | [0]                  | 0         | còn 1 phần tử |

    Nhìn bước 2: chọn -4 (trái) → left nhảy từ 0 lên 1. Nhưng right VẪN Ở 3,
    vì nums[3] = 3 CHƯA ĐƯỢC DÙNG — nó sẽ là ứng viên ở bước 3. Nếu bước 2
    ta cũng right -= 1 (về 2), ta sẽ BỎ SÓT SỐ 3 → kết quả thiếu 9.

    QUY TẮC VÀNG: Chỉ di chuyển con trỏ CỦA BÊN VỪA ĐƯỢC CHỌN. Bên còn lại
    giữ nguyên vì phần tử của nó vẫn "chưa xử lý".

--- Điều gì xảy ra nếu làm SAI? -----------------------------------------
    ❌ Sai 1: Không di chuyển con trỏ nào
        if abs(nums[left]) > abs(nums[right]):
            res[index] = nums[left] ** 2
            # quên left += 1
        else:
            res[index] = nums[right] ** 2
            # quên right -= 1
        → left, right không đổi → vòng lặp CHẠY MÃI (infinite loop) → TLE.
          Nếu có ai đó thêm index -= 1 thì index chạy âm → IndexError.

    ❌ Sai 2: Di chuyển CẢ HAI con trỏ mỗi lần
        if abs(nums[left]) > abs(nums[right]):
            res[index] = nums[left] ** 2
        else:
            res[index] = nums[right] ** 2
        left += 1
        right -= 1     # LUÔN giảm cả hai
        → Mỗi vòng lặp "tiêu thụ" 2 phần tử nhưng chỉ GHI 1 GIÁ TRỊ vào res
          → MẤT MỘT NỬA DỮ LIỆU. Ví dụ [-4,-1,0,3,10] (5 phần tử) sẽ chỉ
          chạy 3 vòng, ghi 3 giá trị, còn res[3], res[4] vẫn là 0 → sai.

    ❌ Sai 3: Di chuyển nhầm bên
        if abs(nums[left]) > abs(nums[right]):
            res[index] = nums[left] ** 2
            right -= 1     # chọn trái nhưng lại giảm phải
        → Phần tử nums[left] được ghi vào res nhưng VẪN NẰM TRONG VÙNG CHƯA
          XỬ LÝ → lần sau có thể CHỌN LẠI → trùng lặp. Đồng thời nums[right]
          bị BỎ QUA dù chưa dùng → thiếu giá trị.

--- Tổng kết bằng 1 câu ------------------------------------------------
    "Con trỏ left (hoặc right) là RANH GIỚI của vùng chưa xử lý. Khi bạn
     lấy phần tử ở đầu nào, ranh giới phía đó PHẢI CO VÀO — nếu không, phần
     tử đã lấy vẫn nằm trong vùng chưa xử lý và sẽ bị lấy lại (hoặc vòng
     lặp không kết thúc)."

--- Sơ đồ trực quan ---------------------------------------------------
    Ban đầu:   [ -4   -1    0    3   10 ]
                 ↑                      ↑
                left                  right
                └──── vùng chưa xử lý ────┘

    Chọn 10 (phải):
               [ -4   -1    0    3  | 10 ]  ← 10 đã xử lý
                 ↑                 ↑
                left             right
                └─ vùng chưa xử lý ─┘         (right co vào)

    Chọn -4 (trái):
               [ -4 | -1    0    3  | 10 ]  ← -4 và 10 đã xử lý
                       ↑           ↑
                      left        right
                      └ vùng chưa ─┘          (left co vào)

    ... tiếp tục cho đến khi left > right → vùng rỗng → xong.


## Độ phức tạp
    - Time  : O(n)
              Vòng lặp chạy đúng n lần (mỗi lần tiêu thụ 1 phần tử từ trái
              hoặc phải). Mỗi lần chỉ có phép so sánh abs, bình phương, gán
              mảng — đều O(1). Tổng: O(n).
    - Space : O(n)
              Mảng "res" bắt buộc phải có n phần tử (output). Không thể ít
              hơn vì đề yêu cầu trả về mảng mới. Space phụ trội (không tính
              output) là O(1) — chỉ 3 biến left, right, index.

    So sánh các cách:
        Brute force (bình phương + sort)  : O(n log n) time, O(n) space
                                            - đơn giản nhưng chậm hơn
        Chia mảng âm/dương rồi merge      : O(n) time, O(n) space
                                            - đúng nhưng code dài, dễ bug
        Two-pointer (cách này)            : O(n) time, O(n) space
                                            - tối ưu nhất, code ngắn, ít bug

    Follow-up của đề: "Tìm giải pháp O(n)" — cách này đáp ứng đúng yêu cầu.
</details>
