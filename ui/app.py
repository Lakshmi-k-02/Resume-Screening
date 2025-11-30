import streamlit as st
import requests

st.set_page_config(page_title="Resume Screening App", layout="wide")
st.title("📄 Resume Screening App")

# Create columns for upload section
col1, col2 = st.columns(2)

with col1:
    st.subheader("📥 Upload Resumes")
    uploaded_resumes = st.file_uploader(
        "Upload Resume(s) - PDF, DOCX, DOC, or TXT", 
        type=["pdf", "docx", "doc", "txt"],
        accept_multiple_files=True
    )
    if uploaded_resumes:
        st.success(f"✅ {len(uploaded_resumes)} file(s) loaded")
        for resume in uploaded_resumes:
            st.caption(f"📄 {resume.name}")

with col2:
    st.subheader("📋 Job Description")
    jd_text = st.text_area("Enter Job Description (Text Form)", height=150)
    if jd_text.strip():
        st.success(f"✅ JD loaded ({len(jd_text.split())} words)")

if st.button("🔍 Process Resumes", use_container_width=True):
    if not uploaded_resumes:
        st.error("❌ Please upload at least one resume file.")
    elif jd_text.strip() == "":
        st.error("❌ Please paste job description text.")
    else:
        with st.spinner(f"Processing {len(uploaded_resumes)} resume(s)..."):
            # Prepare files for multipart upload
            files = []
            for resume in uploaded_resumes:
                file_bytes = resume.read()
                files.append(("resumes", (resume.name, file_bytes, "application/octet-stream")))

            response = requests.post(
                "http://127.0.0.1:8000/screening/",
                data={"jd_text": jd_text},
                files=files
            )

            if response.status_code == 200:
                data = response.json()
                total = data.get("total_processed", 0)
                st.success(f"✅ Successfully processed {total} resume(s)!")
                
                results = data.get("results", [])
                
                # Summary Statistics
                st.markdown("---")
                st.subheader("📊 Summary Statistics")
                
                selected_count = sum(1 for r in results if r.get("status") == "Selected")
                rejected_count = sum(1 for r in results if r.get("status") == "Rejected")
                avg_match = sum(r.get("match_percentage", 0) for r in results if "match_percentage" in r) / len([r for r in results if "match_percentage" in r]) if results else 0
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Processed", len(results))
                with col2:
                    st.metric("🟢 Selected", selected_count)
                with col3:
                    st.metric("🔴 Rejected", rejected_count)
                with col4:
                    st.metric("Avg Match %", f"{avg_match:.1f}%")
                
                # Individual Results
                st.markdown("---")
                st.subheader("📋 Individual Results")
                
                for idx, result in enumerate(results, 1):
                    if "error" in result:
                        with st.expander(f"❌ {result['filename']} - Error", expanded=False):
                            st.error(f"Error: {result['error']}")
                    else:
                        # Determine status emoji
                        status = result.get("status", "Unknown")
                        status_emoji = "🟢" if status == "Selected" else "🔴"
                        match_pct = result.get("match_percentage", 0)
                        
                        with st.expander(
                            f"{status_emoji} {result['filename']} - {status} ({match_pct}%)",
                            expanded=(idx == 1)  # Expand first result by default
                        ):
                            # Main Decision
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Status", status_emoji + " " + status)
                            with col2:
                                st.metric("Skills Match", f"{match_pct}%")
                            with col3:
                                st.write(f"**Feedback:** {result.get('feedback', 'N/A')}")
                            
                            # Candidate Details
                            st.write("---")
                            st.write("**👤 Candidate Details:**")
                            candidate = result.get("candidate_details", {})
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.write(f"**Name:** {candidate.get('name', 'N/A')}")
                            with col2:
                                st.write(f"**Experience:** {candidate.get('experience', 'N/A')}")
                            with col3:
                                st.write(f"**Skills Count:** {len(candidate.get('skills', []))}")
                            
                            st.write(f"**Skills Found:** {', '.join(candidate.get('skills', [])) or 'None'}")
                            
                            # JD Requirements
                            st.write("---")
                            st.write("**💼 Job Requirements:**")
                            jd = result.get("jd_details", {})
                            
                            st.write(f"**Required Experience:** {jd.get('experience_required', 'N/A')}")
                            st.write(f"**Required Skills:** {', '.join(jd.get('skills_required', [])) or 'None'}")
                            
                            # Skills Matching Analysis
                            st.write("---")
                            st.write("**🎯 Skills Analysis:**")
                            
                            matched_skills = result.get("matched_skills", [])
                            missing_skills = result.get("missing_skills", [])
                            
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.write("✅ **Matched Skills:**")
                                if matched_skills:
                                    for skill in matched_skills:
                                        st.success(f"  • {skill.title()}")
                                else:
                                    st.info("  No matched skills")
                            
                            with col2:
                                st.write("❌ **Missing Skills:**")
                                if missing_skills:
                                    for skill in missing_skills:
                                        st.error(f"  • {skill.title()}")
                                else:
                                    st.success("  All required skills present!")
                
            else:
                st.error("❌ Error processing resumes")
                st.write(response.text)
