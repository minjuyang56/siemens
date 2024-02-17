import random

def generate_secret_number():
    return ''.join(random.sample('0123456789', 4))

def check_guess(secret, guess):
    strike = 0
    ball = 0

    for i in range(4):
        if guess[i] == secret[i]:
            strike += 1
        elif guess[i] in secret:
            ball += 1

    return strike, ball

def main():
    print("숫자야구게임을 시작합니다!")

    secret_number = generate_secret_number()
    attempts = 0

    while True:
        user_guess = input("4자리 숫자를 입력하세요: ")

        if len(user_guess) != 4 or not user_guess.isdigit():
            print("올바른 형식의 입력이 아닙니다. 4자리 숫자를 입력해주세요.")
            continue

        attempts += 1

        strike, ball = check_guess(secret_number, user_guess)

        print('결과')
        print(f"{strike} 스트라이크, {ball} 볼")

        if strike == 4:
            print(f"축하합니다! {attempts}번 만에 정답을 맞추셨습니다.")
            break

if __name__ == "__main__":
    main()
