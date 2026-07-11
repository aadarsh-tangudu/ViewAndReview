import streamlit as st
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import time

# ==========================================
# 1. CUSTOM DESIGN SYSTEM & PREMIUM CSS
# ==========================================
st.set_page_config(
    page_title="UI Reviewer - Automated Design Audit",
    page_icon="🎨",
    layout="wide",
)

# Custom premium styling (Dark-glassmorphism theme & neat layout)
st.markdown("""
<style>
    /* Main body customization */
    .stApp {
        background: radial-gradient(circle at 20% 30%, #1c1f26 0%, #111317 100%);
        color: #e2e8f0;
    }
    
    /* Header layout styling */
    .main-header {
        font-size: 2.8rem;
        font-weight: 800;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .sub-header {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    }
    
    /* Card design for layout issues */
    .issue-card {
        background: rgba(30, 41, 59, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
        margin-bottom: 0.8rem;
        backdrop-filter: blur(10px);
    }
    
    .issue-title-critical {
        color: #ef4444;
        font-weight: 700;
        font-size: 1rem;
    }
    
    .issue-title-warning {
        color: #f59e0b;
        font-weight: 700;
        font-size: 1rem;
    }
    
    .issue-desc {
        color: #cbd5e1;
        font-size: 0.9rem;
        margin-top: 0.3rem;
    }
    
    .recommendation-text {
        font-style: italic;
        color: #10b981;
        font-size: 0.85rem;
        margin-top: 0.2rem;
    }
    
    /* Metric container styling */
    .metric-container {
        background: rgba(139, 92, 246, 0.1);
        border: 1px solid rgba(139, 92, 246, 0.2);
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .metric-value {
        font-size: 3rem;
        font-weight: 900;
        color: #a78bfa;
    }
</style>
""", unsafe_allow_html=True)


# ==========================================
# 2. DUMMY MODELS PIPELINE (Mock Logic)
# ==========================================
class DummyUIReviewer:
    """
    Simulates the full machine learning and geometry pipeline:
    1. DETR Component Detection
    2. OCR Text Extraction
    3. Heuristic Rules (Spacing, Alignment, Typography, Contrast)
    4. ViT Quality Scoring
    """
    def __init__(self):
        # UI Component Color Palette for drawing bounding boxes
        self.color_palette = {
            "Button": (59, 130, 246),      # Blue
            "InputField": (236, 72, 153),  # Pink
            "Card": (139, 92, 246),        # Purple
            "Navbar": (16, 185, 129),      # Green
            "Text": (245, 158, 11)         # Amber
        }
        
    def run_pipeline(self, image: Image.Image):
        """
        Runs mock modules and returns detections and issues.
        """
        width, height = image.size
        
        # 1. Simulate DETR detections (bounding boxes relative to image size)
        # BBoxes represented as: [xmin, ymin, xmax, ymax]
        detections = [
            {"class": "Navbar", "bbox": [0, 0, width, int(height * 0.08)], "score": 0.98},
            {"class": "Card", "bbox": [int(width * 0.05), int(height * 0.15), int(width * 0.95), int(height * 0.85)], "score": 0.95},
            {"class": "InputField", "bbox": [int(width * 0.1), int(height * 0.35), int(width * 0.9), int(height * 0.45)], "score": 0.89},
            {"class": "Button", "bbox": [int(width * 0.1), int(height * 0.7), int(width * 0.45), int(height * 0.78)], "score": 0.92},
            {"class": "Button", "bbox": [int(width * 0.55), int(height * 0.7), int(width * 0.9), int(height * 0.78)], "score": 0.91}
        ]
        
        # 2. Simulate OCR extracting text from buttons and input fields
        ocr_results = [
            {"bbox": detections[0]["bbox"], "text": "Dashboard Home Settings"},
            {"bbox": detections[2]["bbox"], "text": "Enter your email address"},
            {"bbox": detections[3]["bbox"], "text": "Cancel"},
            {"bbox": detections[4]["bbox"], "text": "Submit Details"}
        ]
        
        # 3. Simulate Design Rule Analysis & Quality Scores
        report = {
            "overall_score": 7.4,
            "classification": "Good",
            "metrics": {
                "Alignment": 8.5,
                "Spacing & Padding": 6.8,
                "Color & Contrast": 5.5,
                "Typography": 8.0,
                "Accessibility": 7.0
            },
            "issues": [
                {
                    "severity": "Critical",
                    "category": "Color & Contrast",
                    "title": "Low Contrast Ratio on Button",
                    "desc": "The 'Cancel' button text (#FFFFFF) against background (#CBD5E1) has a contrast ratio of 2.1:1. Minimum WCAG AA requirement is 4.5:1.",
                    "recommendation": "Change the background color to a darker gray (#64748B) or increase the text weight."
                },
                {
                    "severity": "Warning",
                    "category": "Spacing & Padding",
                    "title": "Uneven Button Alignment",
                    "desc": "The 'Cancel' and 'Submit Details' buttons have inconsistent spacing. Gap to card edge: Left Button = 48px, Right Button = 54px.",
                    "recommendation": "Set symmetrical padding values on both left and right edges (e.g., margins: 48px)."
                },
                {
                    "severity": "Warning",
                    "category": "Accessibility",
                    "title": "Small Touch Target",
                    "desc": "The 'Cancel' button height is 38px (less than the recommended 48px mobile touch target).",
                    "recommendation": "Increase the button height to 48px and add a minimum padding of 8px around target."
                }
            ]
        }
        
        return detections, ocr_results, report

    def draw_detections(self, image: Image.Image, detections):
        """
        Draws colored bounding boxes with class labels.
        """
        annotated_img = image.copy()
        draw = ImageDraw.Draw(annotated_img)
        
        for det in detections:
            cls = det["class"]
            bbox = det["bbox"]
            score = det["score"]
            color = self.color_palette.get(cls, (255, 255, 255))
            
            # Draw box outlines
            draw.rectangle(bbox, outline=color, width=4)
            
            # Label background & text
            text = f"{cls} ({score:.2f})"
            # Simple fallback text drawing (no custom font file needed)
            x1, y1, x2, y2 = bbox
            draw.rectangle([x1, y1 - 20 if y1 > 20 else y1, x1 + 120, y1], fill=color)
            draw.text((x1 + 5, y1 - 17 if y1 > 20 else y1 + 2), text, fill=(255, 255, 255))
            
        return annotated_img


# Initialize Pipeline
reviewer = DummyUIReviewer()


# ==========================================
# 3. STREAMLIT USER INTERFACE
# ==========================================
st.markdown('<div class="main-header">UI Reviewer</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Upload a screenshot to run a deep learning design audit (DETR + OCR + Heuristics + ViT).</div>', unsafe_allow_html=True)

# File Uploader
uploaded_file = st.file_uploader("Choose a UI Screenshot...", type=["png", "jpg", "jpeg"])

if uploaded_file is not None:
    # Load Image
    image = Image.open(uploaded_file).convert("RGB")
    
    # Grid layout for original vs annotated
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Original Screenshot")
        st.image(image, use_container_width=True)
        
    with col2:
        st.subheader("Automated Component Detection")
        # Spinner to simulate GPU model latency
        with st.spinner("Running DETR component detector, OCR, and ViT scorers..."):
            time.sleep(1.8)  # Mimic inference time
            detections, ocr_results, report = reviewer.run_pipeline(image)
            annotated_img = reviewer.draw_detections(image, detections)
            
        st.image(annotated_img, use_container_width=True)
        
    st.markdown("---")
    
    # Reports and Analytics section
    st.subheader("Design Audit Report")
    
    # Columns for overall score and metrics
    rep_col1, rep_col2 = st.columns([1, 3])
    
    with rep_col1:
        # Score card widget
        score = report["overall_score"]
        classification = report["classification"]
        st.markdown(f"""
        <div class="metric-container">
            <h3>Overall UI Score</h3>
            <div class="metric-value">{score} / 10</div>
            <strong style="color:#a78bfa; font-size:1.2rem;">{classification}</strong>
        </div>
        """, unsafe_allow_html=True)
        
        # Sub-score sliders (Read-only representation)
        st.write("**Model Sub-Scores:**")
        for metric, val in report["metrics"].items():
            st.slider(metric, 0.0, 10.0, float(val), disabled=True)
            
    with rep_col2:
        st.write("### 🚨 Detected Design Issues")
        
        # Display list of layout and color issues
        for issue in report["issues"]:
            severity_class = "issue-title-critical" if issue["severity"] == "Critical" else "issue-title-warning"
            badge = "🔴 CRITICAL" if issue["severity"] == "Critical" else "🟡 WARNING"
            
            st.markdown(f"""
            <div class="issue-card">
                <div class="{severity_class}">
                    {badge} | {issue['category']} - {issue['title']}
                </div>
                <div class="issue-desc">{issue['desc']}</div>
                <div class="recommendation-text">💡 <strong>Recommendation:</strong> {issue['recommendation']}</div>
            </div>
            """, unsafe_allow_html=True)

else:
    # Sidebar guidelines when no image uploaded
    st.info("👈 Please upload a screenshot (Mobile or Web) in the sidebar or drop area to begin.")
    
    # Show dummy placeholder guidelines
    st.markdown("""
    ### What happens behind the scenes:
    1. **Preprocessing**: The screenshot is normalized, scaled, and device orientation is classified.
    2. **DETR Model**: Locates interactive blocks (Buttons, Inputs, Cards, Headers).
    3. **OCR (PaddleOCR)**: Scans for copy texts inside buttons, headings, and labels.
    4. **Layout Auditor**: Runs geometric checks (margins, center-alignments, margins, gaps).
    5. **ViT (Vision Transformer)**: Passes image patch embeddings through quality classification heads.
    """)
