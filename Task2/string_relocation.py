def find_largest_combination(A, B):
    # A의 각 자릿수를 리스트로 변환
    digits = [int(digit) for digit in str(A)]

    # 순열을 생성하여 B보다 작은 가장 큰 수를 찾음
    found = False
    permuts = sorted(permutations(digits, len(digits)), reverse = True)
    for perm in permuts:
        current_number = int(''.join(map(str, perm)))
        if current_number < B:
            found = True
            break

    if found:
        return current_number
    else:
        return 0

from itertools import permutations

if __name__ == "__main__":
    try:
        A = int(input("A를 입력하세요 (3자리 이상): "))
        B = int(input("B를 입력하세요 (A와 다른 숫자로): "))

        if len(str(A)) < 3 or len(str(B)) < 3 or A == B:
            raise ValueError("올바른 입력이 아닙니다.")

        result = find_largest_combination(A, B)

        if result != 0:
            print(f"B보다 작은 가장 큰 수: {result}")
        else:
            print("적절한 값을 찾을 수 없습니다.")
    except ValueError as e:
        print(f"에러: {e}")
