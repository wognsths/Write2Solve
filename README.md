# Write2Solve - 수학 방정식 OCR 및 솔루션 검증 도구

## 프로젝트 개요
Write2Solve는 손으로 쓴 수학 방정식을 인식하고 LaTeX 형식으로 변환한 후, 사용자가 입력한 풀이를 검증해주는 애플리케이션입니다. OCR(광학 문자 인식) 기술과 OpenAI의 o3-mini 모델을 활용하여 정확한 수식 인식과 풀이 검증을 제공합니다.

## 주요 기능
1. **수식 이미지 캡처 및 저장**: 손으로 쓴 수학 방정식을 사진으로 찍어 업로드하면 고유 ID와 함께 저장됩니다.
2. **OCR을 통한 수식 인식**: 업로드된 이미지에서 수학 방정식을 인식하여 LaTeX 형식으로 변환합니다.
3. **수식 편집**: 인식된 수식을 사용자가 직접 수정할 수 있습니다.
4. **솔루션 검증**: 사용자가 입력한 풀이를 AI 모델을 활용하여 검증하고 피드백을 제공합니다.

## 시스템 구조
- **Frontend**: 사용자 인터페이스 제공
- **Backend**: FastAPI 기반 REST API 제공
  - OCR 서비스: 이미지에서 수식 인식
  - LaTeX 서비스: 수식 렌더링 및 검증
  - 저장소 서비스: 이미지, 수식, 솔루션 데이터 관리
  - 추론 서비스: OpenAI의 o3-mini 모델을 활용한 솔루션 검증

## 설치 및 실행 방법

### 사전 요구사항
- Docker 및 Docker Compose
- OpenAI API 키 (o3-mini 모델 사용)

### 환경 설정
1. 프로젝트 클론
   ```bash
   git clone https://github.com/yourusername/Write2Solve.git
   cd Write2Solve
   ```

2. 환경 변수 설정
   - `.env` 파일을 생성하고 다음 내용 추가:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ```

### 실행 방법
1. Docker Compose로 실행
   ```bash
   docker-compose up -d
   ```

2. 브라우저에서 접속
   - 프론트엔드: http://localhost:3000
   - API 문서: http://localhost:8000/docs

## API 엔드포인트
- `POST /api/v1/ocr/`: 이미지 업로드 및 OCR 처리
- `PUT /api/v1/equations/{equation_id}`: 수식 수정
- `POST /api/v1/solutions/`: 솔루션 저장 및 검증
- `POST /api/v1/verify/`: 수식 풀이 검증

## 데이터 저장 구조
- `data/images/`: 업로드된 이미지 저장
- `data/equations/`: 인식된 수식 저장
- `data/solutions/`: 사용자 솔루션 저장
- `data/corrections/`: OCR 모델 개선을 위한 데이터 저장

## 라이선스
MIT License