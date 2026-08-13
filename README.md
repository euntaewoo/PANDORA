# PANDORA - 클라우드 가상 개발 환경 (Docker 활성화)

이 프로젝트는 깃허브 코드스페이스(GitHub Codespaces)를 실행할 때 도커(Docker)가 서버에 자동으로 설치되도록 설계된 설정 환경입니다.

## 🚀 깃허브 코드스페이스 실행 방법

1. 깃허브 저장소(https://github.com/euntaewoo/PANDORA) 웹페이지에 접속합니다.
2. 우측 상단의 **[Code]** 초록색 버튼을 클릭합니다.
3. **[Codespaces]** 탭을 선택하고 **[Create codespace on main]**을 클릭합니다.
4. 웹 브라우저 안에 온라인 가상 서버가 켜지며, `.devcontainer/devcontainer.json` 파일의 지시에 따라 **도커(Docker) 엔진이 백그라운드에 자동으로 무상 설치**됩니다.
5. 터미널 창에 `docker --version`을 입력하여 설치 완료된 도커를 바로 사용하시면 됩니다!
