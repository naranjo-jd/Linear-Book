# Quick Start Guide: Interactive Linear Algebra Book

## 🎯 What You Have

A complete interactive learning platform for linear algebra with:
- ✅ Backend API for solution verification
- ✅ Frontend components for problem submission
- ✅ Demo workshop with working examples
- ✅ Support for code execution, math answers, and multiple choice

## 🚀 Getting Started (Local Development)

### 1. Start the Backend API

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 run.py
```

The API will run on: `http://localhost:8000`
Documentation at: `http://localhost:8000/docs`

### 2. Test the Demo Workshop

Open `talleres/taller-interactive-demo.qmd` in your browser or with Quarto:

```bash
quarto render talleres/taller-interactive-demo.qmd
```

Then open the generated HTML file and:
1. Write Python code or mathematical answers
2. Click "Submit" or "Enviar"
3. See instant feedback

### 3. Try the 3 Built-in Examples

**Problem 1: NumPy Vector Sum**
- Write code to sum a vector [1, 2, 3]
- Expected output: 6
- Status: Ready to test

**Problem 2: Dot Product**  
- Calculate: (1, 2) · (3, 4)
- Expected answer: 11
- Status: Ready to test

**Problem 3: Matrix Determinant**
- Calculate determinant of [[1,2],[3,4]]
- Expected output: -2
- Status: Ready to test

## 📋 Project Structure

```
lineal_2025_2/
├── backend/                    # FastAPI server
│   ├── app/
│   │   ├── routes/            # API endpoints
│   │   ├── services/          # Grading logic
│   │   ├── models.py          # Database models
│   │   └── config.py          # Settings
│   ├── run.py                 # Start server
│   └── requirements.txt
├── frontend-components/        # Reusable widgets
│   ├── code-submission.html
│   └── math-submission.html
├── talleres/
│   ├── taller-interactive-demo.qmd    # ← START HERE
│   ├── taller1.qmd
│   └── ...
├── sections/                   # Course content
│   ├── section0.qmd
│   └── ...
└── README.md
```

## 🔧 Key Files

### Backend
- `backend/app/routes/submissions.py` - Handles code/math submissions
- `backend/app/services/grader.py` - Grading logic
- `backend/app/models.py` - Problem and Submission database models

### Frontend
- `frontend-components/code-submission.html` - Code problem widget
- `frontend-components/math-submission.html` - Math problem widget

### Demo
- `talleres/taller-interactive-demo.qmd` - Complete working example

## 🛠 Common Tasks

### Add a New Problem

1. **Create problem in database**:
```python
from app.db import SessionLocal
from app.models import Problem

db = SessionLocal()
problem = Problem(
    section="taller1",
    problem_id="VF1",
    title="My Problem",
    description="Description here",
    problem_type="code",
    expected_output="42"
)
db.add(problem)
db.commit()
db.close()
```

2. **Add to workshop** (copy-paste from taller-interactive-demo.qmd)

3. **Test** by submitting an answer

### Convert Existing Workshop to Interactive

1. Open existing `talleres/tallerX.qmd`
2. Copy problem submission HTML blocks from `taller-interactive-demo.qmd`
3. Add problem metadata to database
4. Update problem IDs to match
5. Test with backend running

### Deploy Backend to Cloud

**Option A: Heroku** (easiest)
```bash
# Install Heroku CLI, then:
cd backend
heroku create your-app-name
heroku config:set DATABASE_URL=postgresql://...
git push heroku main
```

**Option B: Railway.app** (recommended)
```bash
# Sign up at railway.app
# Connect GitHub repo
# Set start command: python3 run.py
# Auto-deploys on push
```

**Option C: AWS**
- Use Elastic Beanstalk or EC2
- See AWS documentation for FastAPI deployment

## 📖 API Reference

### Submit Code
```bash
curl -X POST http://localhost:8000/api/v1/submit/code \
  -H "Content-Type: application/json" \
  -d '{
    "problem_id": "numpy_sum",
    "code": "import numpy as np\nprint(1+1)"
  }'
```

Response:
```json
{
  "submission_id": 1,
  "problem_id": "numpy_sum",
  "is_correct": false,
  "feedback": "Expected: 6\n\nGot: 2",
  "score": 0.0,
  "execution_output": "2",
  "execution_error": null
}
```

### Submit Math Answer
```bash
curl -X POST http://localhost:8000/api/v1/submit/math \
  -H "Content-Type: application/json" \
  -d '{
    "problem_id": "dot_product",
    "answer": "11"
  }'
```

Response:
```json
{
  "submission_id": 2,
  "problem_id": "dot_product",
  "is_correct": true,
  "feedback": "Correct!",
  "score": 1.0
}
```

## 🐛 Troubleshooting

### "Cannot reach API" error
- Make sure backend is running: `python3 run.py`
- Check it's on port 8000: `curl http://localhost:8000/api/v1/health`
- Check browser console (F12) for errors

### Code submission always fails
- Backend might have timed out (10 second limit)
- Code might be too long (5000 char limit)
- Check backend logs for detailed error

### Database errors
- SQLite database created automatically in `backend/test.db`
- Delete it to reset: `rm backend/test.db`
- Backend will recreate it on next run

## 📚 Next Steps

### Short Term
1. ✅ Test the demo workshop locally
2. Deploy backend to production
3. Update API URL in frontend components
4. Add more problems to database

### Medium Term
5. Convert existing 10 workshops to interactive
6. Add student authentication
7. Create progress tracking dashboard

### Long Term (Phase 2)
8. Add AI/ML focused sections
9. Create ML-specific workshops
10. Enhance existing sections with ML examples

## 📞 Questions?

### Architecture
See `IMPLEMENTATION_PROGRESS.md` for detailed architecture diagrams

### Phase 1 Details
See `PHASE1_SUMMARY.md` in session folder for complete implementation summary

### Plan & Roadmap
See `plan.md` in session folder for full planning document

## 🎓 For Students

Once the system is deployed:

1. **Access the book** at the course website
2. **Read theory sections** to learn concepts
3. **Try workshop problems** with interactive verification
4. **Get instant feedback** on your solutions
5. **Review explanations** if you get it wrong
6. **Track your progress** (coming soon)

---

**Status**: Phase 1 Complete ✅  
**Ready for**: Testing, Deployment, Phase 2  
**Repository**: https://github.com/naranjo-jd/Linear-Book
