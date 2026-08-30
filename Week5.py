"""
5주차 자가진단 — 내 저장소가 남에게 보여줄 만한 상태인가?

사용법:
    cd ~/DEV/ai-study
    python week5_check.py

이번 주는 새 코드를 짜는 주가 아닙니다.
지금까지 만든 것을 '남이 볼 수 있는 상태'로 정리하는 주입니다.

이 스크립트는 채점기가 아니라 점검표입니다.
❌ 가 나오면 바로 아래 안내대로 고치고 다시 돌리세요.
"""

import os
import re
import subprocess


def git(*args):
    """git 명령을 실행하고 결과 문자열을 돌려줍니다. 실패하면 None."""
    try:
        out = subprocess.run(
            ["git"] + list(args),
            capture_output=True, text=True, timeout=15,
        )
        if out.returncode != 0:
            return None
        return out.stdout.strip()
    except Exception:
        return None


PASS, FAIL, WARN = "✅", "❌", "⚠️ "
results = []


def report(ok, title, advice=""):
    mark = PASS if ok else FAIL
    print(f"  {mark} {title}")
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


def main():
    print("\n5주차 저장소 점검\n" + "─" * 52)

    # ── 0. git 저장소인가 ──────────────────────────
    print("\n[기본]")
    if git("rev-parse", "--git-dir") is None:
        report(False, "git 저장소가 아닙니다", """
지금 폴더에서 git이 동작하지 않습니다.
ai-study 폴더로 이동했는지 확인하세요:  pwd
아직 시작 전이라면:                     git init""")
        print("\n먼저 이것부터 해결하고 다시 돌려주세요.\n")
        return

    print(f"  {PASS} git 저장소입니다")

    # ── 1. 커밋 개수 ──────────────────────────────
    print("\n[커밋]")
    count_raw = git("rev-list", "--count", "HEAD")
    count = int(count_raw) if count_raw and count_raw.isdigit() else 0
    report(count >= 10, f"커밋 {count}개 (10개 이상 목표)", """
커밋이 부족합니다. 몰아서 만들지 말고, 실제로 작업을 쪼개세요.
예: 2~4주차 연습 파일을 하나씩 따로 커밋, README 추가를 별도 커밋,
    .gitignore 추가를 별도 커밋.
    git add week2_practice.py
    git commit -m "2주차 연습 문제 풀이 추가" """)

    # ── 2. 커밋 메시지 품질 ────────────────────────
    log = git("log", "--pretty=%s") or ""
    msgs = [m for m in log.split("\n") if m.strip()]
    lazy_pattern = re.compile(r"^(수정|update|updated|fix|test|ㅇㅇ|asdf|커밋|commit|\.+)$", re.I)
    lazy = [m for m in msgs if len(m.strip()) < 6 or lazy_pattern.match(m.strip())]
    if msgs:
        ok = len(lazy) <= len(msgs) * 0.3
        report(ok, f"커밋 메시지 {len(msgs)}개 중 성의 없는 것 {len(lazy)}개", """
'수정', 'update' 같은 메시지는 6개월 뒤의 나에게 아무것도 알려주지 않습니다.
무엇을 왜 바꿨는지 한 줄로 쓰세요.
    나쁨: "수정"
    좋음: "단어 빈도에서 구두점 제거 로직 추가" """)
        if lazy:
            print(f"       (예: {', '.join(repr(m) for m in lazy[:3])})")

    # ── 3. .gitignore ─────────────────────────────
    print("\n[정리 상태]")
    ignore = ""
    if os.path.exists(".gitignore"):
        with open(".gitignore", "r", encoding="utf-8") as f:
            ignore = f.read()
    report(bool(ignore), ".gitignore 파일이 있습니다", """
.gitignore가 없습니다. 만드세요:
    cat > .gitignore <<'EOF'
    .venv/
    __pycache__/
    *.pyc
    .DS_Store
    .env
    EOF""")

    if ignore:
        need = [".venv", "__pycache__", ".env"]
        missing = [n for n in need if n not in ignore]
        report(not missing, f".gitignore에 필수 항목이 들어 있습니다"
                            + (f" (빠진 것: {', '.join(missing)})" if missing else ""), """
빠진 항목을 .gitignore에 추가하세요.
.env 는 나중에 API 키를 넣을 파일입니다. 지금 막아두지 않으면
5단계에서 키가 그대로 GitHub에 올라가고, 남이 내 돈을 씁니다.""")

    tracked = git("ls-files") or ""
    junk = [f for f in tracked.split("\n")
            if f.startswith(".venv/") or "__pycache__" in f or f.endswith(".pyc")
            or f == ".env" or f.endswith("/.env")]
    report(not junk, f"쓰레기 파일이 추적되지 않고 있습니다"
                     + (f" ({len(junk)}개 발견)" if junk else ""), f"""
이미 git에 올라간 파일은 .gitignore를 나중에 써도 계속 따라다닙니다.
목록에서 빼주세요 (파일 자체는 안 지워집니다):
    git rm -r --cached .venv __pycache__
    git commit -m "가상환경과 캐시를 추적 대상에서 제외"
발견된 예: {junk[:3] if junk else ''}""")

    # ── 4. 브랜치 ─────────────────────────────────
    print("\n[브랜치]")
    merges = git("log", "--merges", "--oneline") or ""
    all_branches = git("branch", "--all") or ""
    branch_count = len([b for b in all_branches.split("\n") if b.strip()])
    did_branch = bool(merges.strip()) or branch_count > 2
    report(did_branch, "브랜치를 만들어 작업해본 흔적이 있습니다", """
아직 브랜치를 안 써보셨습니다. 이번 주에 한 번은 해보세요:
    git switch -c feature/readme      # 새 가지에서 작업 시작
    (README 수정하고)
    git add . && git commit -m "README 작성"
    git switch main                   # 원래 가지로 돌아와서
    git merge feature/readme          # 작업을 합치기
혼자 할 땐 없어도 되지만, 팀에서는 이게 기본입니다.""")

    # ── 5. README ─────────────────────────────────
    print("\n[README]")
    readme_path = None
    for name in ("README.md", "readme.md", "README.MD"):
        if os.path.exists(name):
            readme_path = name
            break

    if not report(bool(readme_path), "README.md 파일이 있습니다", """
README가 없으면 GitHub에서 저장소를 열었을 때 파일 목록만 보입니다.
방문자는 3초 안에 나가버립니다. README_template.md를 참고해서 만드세요."""):
        readme = ""
    else:
        with open(readme_path, "r", encoding="utf-8") as f:
            readme = f.read()

    if readme:
        report(len(readme) >= 300, f"내용이 충분합니다 ({len(readme)}자, 300자 이상 목표)", """
너무 짧습니다. 최소한 이 세 가지는 들어가야 합니다:
    1. 이게 무엇인가 / 왜 만들었나
    2. 어떻게 설치하나
    3. 어떻게 실행하나""")

        has_install = any(k in readme for k in ("pip install", "설치", "venv", "requirements"))
        report(has_install, "설치 방법이 적혀 있습니다", """
처음 온 사람이 따라 할 수 있게 설치 명령을 그대로 적어주세요.
    ## 설치
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```""")

        has_run = any(k in readme for k in ("python ", "실행", "사용법", "Usage"))
        report(has_run, "실행 방법이 적혀 있습니다", """
    ## 실행
    ```bash
    python week3_practice.py
    ```""")

        has_code_block = "```" in readme
        report(has_code_block, "코드 블록(```)을 써서 명령을 구분했습니다", """
명령어는 ``` 로 감싸세요. 그냥 쓰면 줄바꿈이 뭉개져서 복사가 안 됩니다.""")

    # ── 6. 원격 저장소 ────────────────────────────
    print("\n[GitHub 연결]")
    remote = git("remote", "-v") or ""
    report("origin" in remote, "GitHub 원격 저장소가 연결되어 있습니다", """
아직 GitHub에 연결되지 않았습니다.
    gh repo create ai-study --public --source=. --push""")

    if "origin" in remote:
        unpushed = git("log", "--oneline", "@{u}..HEAD")
        if unpushed is None:
            warn("업스트림 브랜치가 설정되지 않았습니다", """
    git push -u origin main""")
        elif unpushed.strip():
            n = len([x for x in unpushed.split("\n") if x.strip()])
            warn(f"아직 push하지 않은 커밋이 {n}개 있습니다", "    git push")
        else:
            print(f"  {PASS} 모든 커밋이 GitHub에 올라가 있습니다")

    # ── 결과 ──────────────────────────────────────
    passed = sum(1 for r in results if r)
    total = len(results)
    print("\n" + "─" * 52)
    print(f"{passed} / {total} 통과")

    if passed == total:
        print("""
저장소가 남에게 보여줄 만한 상태입니다.

이번 주의 진짜 의미: 지금까지 만든 코드는 '작동하는 것'이었지만,
이제 '남이 이해할 수 있는 것'이 되었습니다.
포트폴리오는 후자만 인정받습니다.

6주차에는 이 저장소를 하나의 완성된 프로젝트로 키웁니다.
""")
    else:
        print("\n❌ 항목의 안내를 따라 고치고 다시 돌려보세요.")
        print("전부 ✅가 되면 6주차로 넘어갑니다.\n")


if __name__ == "__main__":
    main()