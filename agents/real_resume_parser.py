"""
Real Resume Parser - Extracts actual data from PDF resumes instead of dummy data
Created for AI Job Application Agents project
"""

import PyPDF2
import pdfplumber
import re
import json
from typing import Dict, List, Any, Optional
import io
from datetime import datetime

class RealResumeParser:
    """Real-time resume parser that extracts actual data from PDF files"""
    
    def __init__(self):
        # Comprehensive skills database
        self.tech_skills = {
            # Programming Languages
            'python', 'javascript', 'java', 'c++', 'c#', 'php', 'ruby', 'go', 'rust', 'swift',
            'kotlin', 'scala', 'typescript', 'dart', 'r', 'matlab', 'perl', 'shell', 'bash',
            'c', 'objective-c', 'lua', 'haskell', 'erlang', 'clojure', 'f#', 'vb.net',
            
            # Web Technologies - Frontend
            'react', 'angular', 'vue.js', 'vue', 'jquery', 'bootstrap', 'tailwind', 'html', 'css',
            'html5', 'css3', 'sass', 'less', 'webpack', 'vite', 'next.js', 'nuxt.js', 'svelte',
            'ember.js', 'backbone.js', 'redux', 'mobx', 'vuex', 'styled-components',
            
            # Web Technologies - Backend
            'node.js', 'express', 'django', 'flask', 'spring', 'laravel', 'rails', 'asp.net',
            'fastapi', 'koa', 'nestjs', 'gin', 'fiber', 'actix', 'rocket', 'axum',
            
            # Databases
            'mysql', 'postgresql', 'mongodb', 'redis', 'sqlite', 'oracle', 'sql server',
            'cassandra', 'elasticsearch', 'dynamodb', 'firebase', 'prisma', 'sequelize',
            'mariadb', 'neo4j', 'couchdb', 'influxdb', 'cockroachdb', 'supabase',
            
            # Cloud & DevOps
            'aws', 'azure', 'gcp', 'google cloud', 'docker', 'kubernetes', 'jenkins',
            'gitlab ci', 'github actions', 'terraform', 'ansible', 'chef', 'puppet',
            'vagrant', 'nginx', 'apache', 'cloudflare', 'vercel', 'netlify', 'heroku',
            
            # Data & AI
            'machine learning', 'deep learning', 'tensorflow', 'pytorch', 'scikit-learn',
            'pandas', 'numpy', 'jupyter', 'tableau', 'power bi', 'spark', 'hadoop',
            'kafka', 'airflow', 'dbt', 'snowflake', 'databricks', 'mlflow', 'kubeflow',
            
            # Mobile Development
            'ios', 'android', 'react native', 'flutter', 'xamarin', 'ionic', 'cordova',
            'unity', 'unreal engine', 'cocos2d', 'phonegap',
            
            # Tools & Others
            'git', 'svn', 'jira', 'confluence', 'slack', 'figma', 'sketch', 'photoshop',
            'linux', 'unix', 'windows', 'macos', 'vim', 'vscode', 'intellij', 'eclipse',
            'postman', 'insomnia', 'swagger', 'graphql', 'rest api', 'soap', 'grpc',
            
            # Testing
            'jest', 'mocha', 'chai', 'cypress', 'selenium', 'junit', 'pytest', 'rspec',
            'cucumber', 'testng', 'mockito', 'sinon', 'enzyme', 'react testing library',
            
            # Project Management & Methodologies  
            'agile', 'scrum', 'kanban', 'waterfall', 'lean', 'six sigma', 'devops',
            'ci/cd', 'tdd', 'bdd', 'pair programming', 'code review'
        }
        
        # Common job titles and experience keywords
        self.experience_keywords = {
            'senior': ['senior', 'sr.', 'lead', 'principal', 'architect', 'head of', 'director'],
            'mid-level': ['developer', 'engineer', 'analyst', 'specialist', 'consultant'],
            'junior': ['junior', 'jr.', 'associate', 'trainee', 'intern', 'entry-level', 'graduate']
        }
        
        # Education keywords
        self.education_keywords = [
            'computer science', 'software engineering', 'information technology', 'computer engineering',
            'electrical engineering', 'mathematics', 'physics', 'data science', 'artificial intelligence',
            'cybersecurity', 'information systems', 'business administration', 'mba', 'bachelor', 'master',
            'phd', 'doctorate', 'degree', 'university', 'college', 'institute'
        ]

    def extract_text_from_pdf(self, pdf_content: bytes) -> str:
        """Extract text from PDF file using multiple methods for better accuracy"""
        text = ""
        
        # Check if content is too small to be a valid PDF
        if len(pdf_content) < 1024:  # Less than 1KB is suspicious
            print(f"⚠️ PDF file is very small ({len(pdf_content)} bytes). May be corrupted.")
        
        # Check basic PDF header
        if not pdf_content.startswith(b'%PDF-'):
            print("❌ File does not have valid PDF header")
            raise Exception("Invalid PDF file format")
        
        try:
            # Method 1: Using pdfplumber (better for complex layouts)
            print("🔍 Trying pdfplumber extraction...")
            with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
                if not pdf.pages:
                    raise Exception("PDF has no pages")
                
                for i, page in enumerate(pdf.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                            print(f"✅ Extracted text from page {i+1}: {len(page_text)} characters")
                    except Exception as e:
                        print(f"⚠️ Failed to extract from page {i+1}: {e}")
                        continue
            
        except Exception as e1:
            print(f"⚠️ pdfplumber failed: {e1}")
            
            # Method 2: Fallback to PyPDF2
            try:
                print("🔍 Trying PyPDF2 extraction...")
                pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_content))
                
                if len(pdf_reader.pages) == 0:
                    raise Exception("PDF has no pages")
                
                for i, page in enumerate(pdf_reader.pages):
                    try:
                        page_text = page.extract_text()
                        if page_text:
                            text += page_text + "\n"
                            print(f"✅ PyPDF2 extracted text from page {i+1}: {len(page_text)} characters")
                    except Exception as e:
                        print(f"⚠️ PyPDF2 failed on page {i+1}: {e}")
                        continue
                        
            except Exception as e2:
                print(f"❌ Both PDF extraction methods failed:")
                print(f"   pdfplumber: {e1}")
                print(f"   PyPDF2: {e2}")
                
                # Method 3: Try to extract as much as possible with character-level extraction
                try:
                    print("🔍 Trying character-level extraction...")
                    with pdfplumber.open(io.BytesIO(pdf_content)) as pdf:
                        for i, page in enumerate(pdf.pages):
                            try:
                                chars = page.chars
                                if chars:
                                    char_text = ''.join([char.get('text', '') for char in chars])
                                    if char_text.strip():
                                        text += char_text + "\n"
                                        print(f"✅ Character extraction from page {i+1}: {len(char_text)} characters")
                            except:
                                continue
                except Exception as e3:
                    print(f"❌ Character-level extraction also failed: {e3}")
                
                if not text.strip():
                    raise Exception("Could not extract any text from PDF file")
        
        extracted_length = len(text.strip())
        print(f"📄 Total extracted text: {extracted_length} characters")
        
        if extracted_length == 0:
            raise Exception("PDF appears to be empty or contains only images/scanned content")
        
        return text.strip()

    def extract_contact_info(self, text: str) -> Dict[str, str]:
        """Extract contact information from resume text"""
        contact_info = {
            'name': '',
            'email': '',
            'phone': '',
            'location': '',
            'linkedin': '',
            'github': ''
        }
        
        lines = text.split('\n')
        
        # Extract email
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text, re.IGNORECASE)
        contact_info['email'] = emails[0] if emails else ""
        
        # Extract phone number (multiple formats)
        phone_patterns = [
            r'(\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',  # US format
            r'(\+?[0-9]{1,3}[-.\s]?)?[0-9]{3,4}[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,4}',  # International
        ]
        for pattern in phone_patterns:
            phones = re.findall(pattern, text)
            if phones:
                # Clean up the phone number
                phone = ''.join(phones[0]) if isinstance(phones[0], tuple) else phones[0]
                contact_info['phone'] = re.sub(r'[^\d+]', '', phone)
                break
        
        # Extract LinkedIn profile
        linkedin_pattern = r'linkedin\.com/in/[\w-]+'
        linkedin_matches = re.findall(linkedin_pattern, text, re.IGNORECASE)
        contact_info['linkedin'] = f"https://{linkedin_matches[0]}" if linkedin_matches else ""
        
        # Extract GitHub profile  
        github_pattern = r'github\.com/[\w-]+'
        github_matches = re.findall(github_pattern, text, re.IGNORECASE)
        contact_info['github'] = f"https://{github_matches[0]}" if github_matches else ""
        
        # Extract name (usually in first few lines, avoid lines with contact info)
        for line in lines[:8]:
            line = line.strip()
            if not line:
                continue
                
            # Skip lines with contact info patterns
            if any(pattern in line.lower() for pattern in 
                   ['email', 'phone', 'tel:', 'mobile:', 'linkedin', 'github', '@', '+', 'http']):
                continue
                
            # Look for name patterns (2-4 words, starts with capital)
            words = line.split()
            if (2 <= len(words) <= 4 and 
                all(word[0].isupper() and word.isalpha() for word in words) and
                len(line) < 50):  # Names shouldn't be too long
                contact_info['name'] = line
                break
        
        # Extract location (look for city, state patterns)
        location_pattern = r'\b[A-Za-z\s]+,\s*[A-Za-z]{2,}\b'
        locations = re.findall(location_pattern, text)
        if locations:
            contact_info['location'] = locations[0]
        
        return contact_info

    def extract_skills(self, text: str) -> List[str]:
        """Extract technical skills from resume text"""
        found_skills = set()
        text_lower = text.lower()
        
        # Look for skills in the entire text
        for skill in self.tech_skills:
            skill_lower = skill.lower()
            # Use word boundaries for better matching
            pattern = r'\b' + re.escape(skill_lower) + r'\b'
            if re.search(pattern, text_lower):
                found_skills.add(skill.title())
        
        # Look for skills in dedicated skills sections
        skills_section_pattern = r'(?i)(skills?|technologies?|technical\s+skills?|programming\s+languages?)[\s\n]*[:\-]?\s*(.{0,500}?)(?=\n\s*[A-Z][a-z]+:|\n\s*\n|$)'
        skills_matches = re.findall(skills_section_pattern, text, re.MULTILINE | re.DOTALL)
        
        for _, skills_content in skills_matches:
            for skill in self.tech_skills:
                if skill.lower() in skills_content.lower():
                    found_skills.add(skill.title())
        
        return sorted(list(found_skills))

    def extract_experience_level(self, text: str) -> Dict[str, Any]:
        """Determine experience level from resume content"""
        text_lower = text.lower()
        
        # Count experience-related keywords
        senior_count = sum(1 for keyword in self.experience_keywords['senior'] 
                          if keyword in text_lower)
        mid_count = sum(1 for keyword in self.experience_keywords['mid-level'] 
                       if keyword in text_lower)
        junior_count = sum(1 for keyword in self.experience_keywords['junior'] 
                          if keyword in text_lower)
        
        # Look for years of experience
        years_pattern = r'(\d+)[\s\-+]*(?:years?|yrs?)[\s\-+]*(?:of\s+)?(?:experience|exp)'
        years_matches = re.findall(years_pattern, text_lower)
        
        total_years = 0
        if years_matches:
            # Get the maximum years mentioned
            years = [int(y) for y in years_matches if y.isdigit()]
            total_years = max(years) if years else 0
        
        # Determine level based on years and keywords
        if total_years >= 7 or senior_count > mid_count + junior_count:
            level = "Senior"
        elif total_years >= 3 or mid_count > junior_count:
            level = "Mid-level"
        else:
            level = "Junior"
        
        return {
            'level': level,
            'years_experience': f"{total_years}+" if total_years > 0 else "Not specified",
            'confidence': 0.8 if total_years > 0 else 0.6
        }

    def extract_education(self, text: str) -> List[str]:
        """Extract education information"""
        education = []
        text_lower = text.lower()
        
        # Look for education section
        education_pattern = r'(?i)(education|academic|qualifications?)[\s\n]*[:\-]?\s*(.{0,800}?)(?=\n\s*[A-Z][a-z]+:|\n\s*\n|$)'
        education_matches = re.findall(education_pattern, text, re.MULTILINE | re.DOTALL)
        
        found_education = set()
        
        # Search in dedicated education sections
        for _, edu_content in education_matches:
            for keyword in self.education_keywords:
                if keyword in edu_content.lower():
                    found_education.add(keyword.title())
        
        # Search in entire document if no dedicated section found
        if not found_education:
            for keyword in self.education_keywords:
                if keyword in text_lower:
                    found_education.add(keyword.title())
        
        return list(found_education)

    def extract_summary(self, text: str) -> str:
        """Generate a summary based on extracted information"""
        lines = text.split('\n')
        
        # Look for summary/objective sections
        summary_patterns = [
            r'(?i)(summary|profile|objective|about|overview)[\s\n]*[:\-]?\s*(.{0,300}?)(?=\n\s*[A-Z][a-z]+:|\n\s*\n|$)',
            r'(?i)(professional\s+summary|career\s+summary|executive\s+summary)[\s\n]*[:\-]?\s*(.{0,300}?)(?=\n\s*[A-Z][a-z]+:|\n\s*\n|$)'
        ]
        
        for pattern in summary_patterns:
            matches = re.findall(pattern, text, re.MULTILINE | re.DOTALL)
            if matches:
                summary = matches[0][1].strip()
                if len(summary) > 50:  # Ensure it's substantial
                    return summary
        
        # Fallback: create summary from first substantial paragraph
        for line in lines[:10]:
            line = line.strip()
            if (len(line) > 100 and 
                not any(pattern in line.lower() for pattern in 
                       ['email', 'phone', 'linkedin', 'github', '@'])):
                return line
        
        return "Professional seeking new opportunities"

    def parse_resume(self, pdf_content: bytes) -> Dict[str, Any]:
        """Main method to parse resume and extract all information"""
        try:
            print("🔍 Starting real resume parsing...")
            
            # Extract text from PDF
            text = self.extract_text_from_pdf(pdf_content)
            if not text:
                raise Exception("Could not extract text from PDF")
            
            print(f"✅ Extracted {len(text)} characters of text")
            
            # Extract all information
            contact_info = self.extract_contact_info(text)
            skills = self.extract_skills(text)
            experience = self.extract_experience_level(text)
            education = self.extract_education(text)
            summary = self.extract_summary(text)
            
            result = {
                "success": True,
                "extracted_at": datetime.now().isoformat(),
                "contact_info": contact_info,
                "skills": skills,
                "experience_level": experience['level'],
                "years_experience": experience['years_experience'],
                "education": education,
                "summary": summary,
                "text_length": len(text),
                "parsing_confidence": experience['confidence']
            }
            
            print(f"✅ Successfully parsed resume:")
            print(f"   📧 Name: {contact_info['name'] or 'Not found'}")
            print(f"   📧 Email: {contact_info['email'] or 'Not found'}")
            print(f"   🔧 Skills found: {len(skills)}")
            print(f"   📈 Experience level: {experience['level']}")
            
            return result
            
        except Exception as e:
            print(f"❌ Error parsing resume: {e}")
            return {
                "success": False,
                "error": str(e),
                "extracted_at": datetime.now().isoformat()
            }

# Test function for development
def test_parser():
    """Test function to validate the parser"""
    parser = RealResumeParser()
    
    # Test with sample text
    sample_text = """
    John Doe
    Software Engineer
    john.doe@email.com | (555) 123-4567 | linkedin.com/in/johndoe
    
    Professional Summary:
    Experienced software developer with 5+ years of experience in Python, React, and cloud technologies.
    
    Technical Skills:
    - Programming Languages: Python, JavaScript, TypeScript
    - Frameworks: React, Django, FastAPI
    - Databases: PostgreSQL, MongoDB, Redis
    - Cloud: AWS, Docker, Kubernetes
    
    Education:
    Bachelor of Science in Computer Science
    University of Technology, 2019
    """
    
    # Simulate PDF content (in real use, this would be actual PDF bytes)
    print("🧪 Testing resume parser with sample data...")
    
    contact = parser.extract_contact_info(sample_text)
    skills = parser.extract_skills(sample_text)
    experience = parser.extract_experience_level(sample_text)
    
    print("📋 Test Results:")
    print(f"   Name: {contact['name']}")
    print(f"   Email: {contact['email']}")
    print(f"   Skills: {skills}")
    print(f"   Experience: {experience}")

if __name__ == "__main__":
    test_parser()