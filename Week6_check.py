"""
6주차 프로젝트 점검 — 뉴스·게시글 수집기

사용법:
    cd ~/DEV/[프로젝트폴더]
    python week6_check.py

이 도구는 코드가 '맞는지'를 보지 않습니다. 그건 실행해보면 아니까요.
대신 남이 봤을 때 프로젝트로 보이는지를 검사합니다.

검사 항목은 채용 담당자가 30초 안에 확인하는 것들과 거의 같습니다.
"""

import ast
import csv
import os
import subprocess


PASS, FAIL, WARN = "✅", "❌", "⚠️ "
results = []
SKIP = ("week2_practice.py", "week3_practice.py", "week4_practice.py",
        "week5_check.py", "week6_check.py", "first_ml.py", "exp.py",
        "look.py", "tree.py", "week2_solution.py")


def report(ok, title, advice=""):
    print(f"  {PASS if ok else FAIL} {title}")
    if not ok and advice:
        for line in advice.strip().split("\n"):
            print(f"       {line}")
    results.append(ok)
    return ok


def warn(title, advice=""):
    print(f"  {WARN}{title}")
    if advice:
        for line in advice.strip().split("\n"):
            print(f"       {line}")


def git(*args):
    try:
        out = subprocess.run(["git"] + list(args), capture_output=True,
                             text=True, timeout=15)
        return out.stdout.strip() if out.returncode == 0 else None
    except Exception:
        return None


def collect_sources():
    """프로젝트 코드 파일만 모읍니다 (연습 파일과 이 검사기는 제외)."""
    files = []
    for name in sorted(os.listdir(".")):
        if name.endswith(".py") and name not in SKIP:
            files.append(name)
    return files


class CodeFacts:
    """코드를 파싱해서 사실만 모읍니다."""

    def __init__(self):
        self.classes = []
        self.functions = []
        self.calls = set()
        self.has_try = False
        self.has_main_guard = False
        self.top_level_statements = 0
        self.parse_errors = []
        self.abs_paths = []

    def scan(self, path):
        with open(path, "r", encoding="utf-8") as f:
            src = f.read()
        try:
            tree = ast.parse(src)
        except SyntaxError as e:
            self.parse_errors.append(f"{path}: {e}")
            return

        for node in tree.body:
            if isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef,
                                 ast.AsyncFunctionDef, ast.ClassDef, ast.If,
                                 ast.Assign, ast.AnnAssign, ast.Expr)):
                if isinstance(node, ast.If):
                    test = ast.dump(node.test)
                    if "__main__" in test:
                        self.has_main_guard = True
                        continue
                if isinstance(node, (ast.Assign, ast.AnnAssign, ast.Expr)):
                    self.top_level_statements += 1
            else:
                self.top_level_statements += 1

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                self.classes.append(node.name)
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                self.functions.append(node.name)
            elif isinstance(node, ast.Try):
                self.has_try = True
            elif isinstance(node, ast.Call):
                self.calls.add(_call_name(node.func))
            elif isinstance(node, ast.Constant) and isinstance(node.value, str):
                v = node.value
                if v.startswith("/Users/") or v.startswith("C:\\"):
                    self.abs_paths.append(v)


def _call_name(func):
    if isinstance(func, ast.Name):
        return func.id
    if isinstance(func, ast.Attribute):
        return _call_name(func.value) + "." + func.attr
    return "?"


def main():
    print("\n6주차 프로젝트 점검\n" + "═" * 52)

    sources = collect_sources()
    if not sources:
        print("\n  ❌ 검사할 .py 파일이 없습니다.")
        print("     프로젝트 폴더에서 실행했는지 확인하세요. (pwd)\n")
        return

    print(f"\n검사 대상: {', '.join(sources)}")

    facts = CodeFacts()
    for path in sources:
        facts.scan(path)

    if facts.parse_errors:
        print("\n  ❌ 문법 오류가 있어 파싱하지 못한 파일이 있습니다:")
        for e in facts.parse_errors:
            print(f"       {e}")
        print()
        return

    # ── 1. 구조 ───────────────────────────────────
    print("\n[구조 — 코드가 정리되어 있는가]")

    report(len(facts.classes) >= 1,
           f"클래스를 사용했습니다 ({len(facts.classes)}개: {', '.join(facts.classes) or '없음'})", """
4주차에 배운 클래스를 써보세요. 이 프로젝트에서 자연스러운 후보:
    class Article:    제목·링크·날짜를 담는 그릇
    class Collector:  수집한 기사를 모아두고 저장하는 역할 (WordCounter와 같은 구조)""")

    report(len(facts.functions) >= 5,
           f"함수로 나눠져 있습니다 ({len(facts.functions)}개, 5개 이상 목표)", """
한 함수가 모든 걸 하고 있으면 고치기 어렵습니다. 역할별로 자르세요:
    fetch_page(url)        페이지 가져오기
    parse_articles(html)   HTML에서 기사 뽑기
    save_csv(rows, path)   파일로 저장
    main()                 전체 흐름""")

    report(facts.has_main_guard,
           'if __name__ == "__main__": 가 있습니다', """
파일 맨 아래에 이 줄을 넣고, 실행 코드를 그 안으로 옮기세요.
    if __name__ == "__main__":
        main()
이게 없으면 남이 이 파일을 import 하는 순간 크롤링이 멋대로 시작됩니다.""")

    report(facts.top_level_statements <= 12,
           f"파일 바깥에 흩어진 코드가 적습니다 ({facts.top_level_statements}줄)", """
함수 밖에 늘어놓은 코드가 많습니다. main() 안으로 넣으세요.
상수(URL, 파일명)는 대문자로 위에 두는 게 좋습니다:  BASE_URL = "..." """)

    # ── 2. 수집기다운 요건 ─────────────────────────
    print("\n[수집기 — 남의 서버를 쓰는 프로그램의 예의]")

    used_requests = any("requests" in c for c in facts.calls)
    report(used_requests, "requests로 페이지를 가져옵니다", """
requests.get(url) 을 써서 실제 페이지를 가져오세요.""")

    has_sleep = any("sleep" in c for c in facts.calls)
    report(has_sleep, "요청 사이에 간격을 둡니다 (time.sleep)", """
반복문 안에서 쉬지 않고 요청하면 상대 서버에 부하를 줍니다.
차단당하는 건 물론이고, 상황에 따라 업무방해가 될 수도 있습니다.
    import time
    time.sleep(1)      # 페이지 하나 가져올 때마다 1초 쉬기
이 한 줄이 '크롤러를 만들 줄 안다'와 '함부로 만든다'를 가릅니다.""")

    report(facts.has_try, "예외처리(try/except)가 있습니다", """
네트워크는 반드시 실패합니다. 페이지 하나가 안 열렸다고
프로그램 전체가 죽으면 안 됩니다.
    try:
        r = requests.get(url, timeout=10)
    except requests.RequestException as e:
        print(f"건너뜀: {url} ({e})")
        continue""")

    has_timeout = "timeout" in open(sources[0], encoding="utf-8").read() or any(
        "timeout" in open(s, encoding="utf-8").read() for s in sources)
    report(has_timeout, "requests에 timeout을 지정했습니다", """
timeout 없이 요청하면 서버가 응답을 안 줄 때 영원히 멈춰 있습니다.
    requests.get(url, timeout=10)""")

    report(not facts.abs_paths,
           "내 컴퓨터에서만 되는 절대경로가 없습니다"
           + (f" ({facts.abs_paths[:1]})" if facts.abs_paths else ""), """
'/Users/내이름/...' 같은 경로는 남의 컴퓨터에서 바로 터집니다.
파일명만 쓰거나, os.path.join 을 쓰세요.""")

    # ── 3. 결과물 ─────────────────────────────────
    print("\n[결과물 — 실제로 뭔가 나오는가]")

    csvs = [f for f in os.listdir(".") if f.endswith(".csv")]
    if report(bool(csvs), f"CSV 결과 파일이 있습니다 ({', '.join(csvs) or '없음'})", """
수집 결과를 CSV로 저장하세요. 8주차 pandas에서 이 파일을 그대로 읽게 됩니다.
    import csv
    with open("articles.csv", "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f)
        w.writerow(["제목", "링크", "날짜"])
        w.writerows(rows)"""):
        target = csvs[0]
        try:
            with open(target, "r", encoding="utf-8-sig") as f:
                rows = list(csv.reader(f))
            report(len(rows) >= 3,
                   f"{target} 에 데이터가 들어 있습니다 (헤더 포함 {len(rows)}줄)", """
수집 결과가 거의 없습니다. 최소 10건 이상은 모아보세요.""")
            if rows:
                header = rows[0]
                looks_like_header = all(
                    not c.strip().replace(".", "").isdigit() for c in header if c.strip())
                report(looks_like_header and len(header) >= 2,
                       f"헤더 행이 있습니다 ({', '.join(header[:4])})", """
첫 줄에 열 이름을 넣으세요. 없으면 나중에 pandas로 읽을 때 첫 데이터가 헤더가 됩니다.""")
        except Exception as e:
            warn(f"{target} 를 읽는 중 문제: {e}")

    # ── 4. 문서와 공개 ────────────────────────────
    print("\n[문서 — 남이 이해할 수 있는가]")

    readme = ""
    for name in ("README.md", "readme.md"):
        if os.path.exists(name):
            with open(name, "r", encoding="utf-8") as f:
                readme = f.read()
            break

    if report(bool(readme), "README.md 가 있습니다",
              "5주차의 README_template.md 를 가져와 채우세요."):
        report(len(readme) >= 500,
               f"내용이 충분합니다 ({len(readme)}자, 500자 이상 목표)", """
6주차 프로젝트 README는 5주차보다 자세해야 합니다.
무엇을 수집하는지, 어떤 사이트를 대상으로 하는지, 결과가 어떻게 생겼는지.""")
        report("```" in readme, "코드 블록으로 명령을 보여줍니다")
        has_image = "![" in readme
        report(has_image, "실행 화면(스크린샷)이 들어 있습니다", """
터미널 실행 장면을 캡처해서 저장소에 올리고 README에 넣으세요.
    ![실행 화면](screenshot.png)
글 열 줄보다 사진 한 장이 빠릅니다.""")
        has_learned = any(k in readme for k in ("배운", "어려", "시행착오", "문제"))
        report(has_learned, "'배운 것 / 어려웠던 것'이 적혀 있습니다", """
이 항목이 다른 학습용 저장소와 나를 가르는 부분입니다.
막혔던 지점과 해결 과정을 구체적으로 쓰세요.""")

    report(os.path.exists("requirements.txt"), "requirements.txt 가 있습니다", """
    pip freeze > requirements.txt
이게 있어야 남이 같은 환경을 만들 수 있습니다.""")

    print("\n[공개]")
    remote = git("remote", "-v") or ""
    report("origin" in remote, "GitHub에 연결되어 있습니다",
           "    gh repo create [프로젝트이름] --public --source=. --push")
    unpushed = git("log", "--oneline", "@{u}..HEAD")
    if "origin" in remote:
        if unpushed and unpushed.strip():
            warn(f"push하지 않은 커밋이 {len(unpushed.splitlines())}개 있습니다", "    git push")

    # ── 결과 ──────────────────────────────────────
    passed = sum(1 for r in results if r)
    total = len(results)
    print("\n" + "═" * 52)
    print(f"{passed} / {total} 통과")

    if passed == total:
        print("""
1단계 완료입니다.

6주 전에는 파이썬 문법만 알고 계셨습니다.
지금은 인터넷에서 데이터를 모아 파일로 남기는 프로그램을 만들고,
그걸 남이 실행할 수 있는 형태로 공개할 수 있습니다.

방금 만든 CSV 파일은 버리지 마세요.
8주차 pandas에서 바로 이 파일을 읽어서 분석하게 됩니다.
내가 모은 데이터로 배우는 것과 남의 예제로 배우는 건 완전히 다릅니다.

다음은 7주차 — NumPy입니다.
""")
    else:
        print("\n❌ 항목을 하나씩 지워나가세요. 전부 ✅면 1단계 완료입니다.\n")


if __name__ == "__main__":
    main()