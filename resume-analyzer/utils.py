import fitz  
import re
from sklearn.feature_extraction.text import ENGLISH_STOP_WORDS


CUSTOM_STOP_WORDS = {
    'experience', 'years', 'working', 'knowledge', 'development', 'team', 
    'required', 'skills', 'ability', 'looking', 'work', 'strong', 'understanding', 
    'using', 'good', 'excellent', 'must', 'have', 'developer', 'engineer', 'role', 
    'job', 'preferred', 'requirements', 'responsibilities', 'opportunity', 
    'opportunities', 'business', 'environment', 'design', 'building', 'create',
    'creating', 'maintain', 'maintaining', 'support', 'supporting', 'including',
    'software', 'application', 'applications', 'system', 'systems', 'solutions',
    'technical', 'technology', 'technologies', 'web', 'data', 'user', 'users',
    'client', 'clients', 'project', 'projects', 'product', 'products', 'services',
    'service', 'management', 'manage', 'managing', 'lead', 'leading', 'develop',
    'developing', 'test', 'testing', 'code', 'coding', 'best', 'practices', 'degree',
    'computer', 'science', 'engineering', 'field', 'related', 'bachelors', 'masters',
    'phd', 'proven', 'track', 'record', 'demonstrated', 'communication',
    'written', 'verbal', 'agile', 'scrum', 'environment', 'fast', 'paced', 'highly',
    'motivated', 'self', 'starter', 'independent', 'collaborative', 'cross', 'functional',
    'teams', 'able', 'proficient', 'proficiency', 'familiar', 'familiarity',
    'plus', 'bonus', 'nice', 'ideal', 'candidate', 'successful', 'join', 'company',
    'expert', 'expertise', 'hands', 'on', 'minimum', 'maximum', 'equivalent', 
    'passionate', 'drive', 'driven', 'impactp', 'deliver', 'delivering', 'focus',
    'focused', 'ensure', 'ensuring', 'quality', 'high', 'perform', 'performance',
    'we', 'our', 'us', 'you', 'your', 'are', 'is', 'a', 'an', 'the', 'of', 'and',
    'to', 'in', 'for', 'with', 'on', 'as', 'by', 'at', 'or', 'from', 'be', 'this',
    'that', 'it', 'can', 'will', 'not', 'but', 'all', 'any', 'other', 'more', 'about',
    'if', 'so', 'up', 'out', 'into', 'has', 'do', 'such', 'only', 'new', 'some', 'well',
    'also', 'very', 'than', 'could', 'should', 'would', 'may', 'might', 'their', 'they',
    'them', 'what', 'which', 'who', 'whom', 'whose', 'where', 'when', 'why', 'how',
    'been', 'being', 'am', 'was', 'were', 'does', 'did', 'done', 'doing', 'having',
    'had', 'got', 'gotten', 'getting', 'give', 'gives', 'gave', 'given', 'giving',
    'make', 'makes', 'made', 'making', 'take', 'takes', 'took', 'taken', 'taking',
    'see', 'sees', 'saw', 'seen', 'seeing', 'look', 'looks', 'looked', 'looking',
    'like', 'likes', 'liked', 'liking', 'want', 'wants', 'wanted', 'wanting', 
    'need', 'needed', 'end', 'handle', 'browser', 'build', 'skilled', 'basic',
    'compatibility', 'interactions','includes','hackathon','additional','certifications','simulation'

    
    'builds', 'built', 'works', 'worked', 'handles', 'handled',
    'uses', 'used', 'utilize', 'utilized',
    'implements', 'implemented', 'implementing',
    'executes', 'executed', 'execution',


    'responsible', 'responsibility',
    'contribute', 'contributing',
    'participate', 'participating',
    'involved', 'involvement',
    'assist', 'assisting',
    'coordinate', 'coordinating',
    'collaborate', 'collaboration',

    
    'hardworking', 'dedicated', 'enthusiastic',
    'detail', 'detail-oriented',
    'multitasking', 'flexible',
    'quick', 'quickly', 'fast-learner',


    'hiring', 'position', 'opening',
    'vacancy', 'apply', 'applying',
    'joiner', 'immediate', 'urgent',

   
    'junior', 'senior', 'mid', 'level',
    'entry', 'fresher', 'experienced',

    
    'platforms', 'framework', 'frameworks',
    'tools', 'tooling', 'stacks', 'ecosystem',

    'various', 'multiple', 'different',
    'several', 'many', 'etc',
    
    'innovative', 'innovate', 'dynamic', 'synergy', 'proactive', 'scalable', 'robust',
    'seamless', 'strategic', 'strategy', 'optimization', 'optimize', 'leveraged',
    'leveraging', 'spearheaded', 'facilitated', 'orchestrated', 'streamlined',
    'analyzed', 'analysis', 'proficiencies', 'competencies', 'methodologies',
    'outstanding', 'exceptional', 'fluency', 'fluent', 'core', 'key', 'impactful',
    'comprehensive', 'deep', 'broad', 'solid', 'proficiently', 'successfully',
    'effectively', 'efficiently', 'significant', 'significantly', 'critical', 'crucial',
    'vital', 'essential', 'necessary', 'advantage', 'beneficial', 'consistently',
    'seeking', 'foundation', 'fundamentals', 'environments', 'possess', 'teamwork',
    'time', 'punctuality', 'considered','person'
}


ALL_STOP_WORDS = ENGLISH_STOP_WORDS.union(CUSTOM_STOP_WORDS)

def extract_text_from_pdf(file):
    text = ""
    pdf = fitz.open(stream=file.read(), filetype="pdf")
    for page in pdf:
        text += page.get_text()
    return text

def extract_targeted_sections(text):
    
    lines = text.split('\n')
    target_text = []
    in_target_section = False
    
    stop_headers = ['summary', 'objective', 'hobbies']
    start_headers = ['skills', 'technical skills', 'core competencies', 'projects', 'academic projects', 'personal projects', 'certifications', 'certification', 'experience', 'work history', 'education', 'achievements', 'languages']
    
    for line in lines:
        cleaned_line = line.strip().lower()
        if not cleaned_line:
            continue
            
        if len(cleaned_line) < 30:
            if any(cleaned_line == sh for sh in start_headers) or any(cleaned_line.startswith(sh) for sh in start_headers):
                in_target_section = True
                continue
            if any(cleaned_line == sh for sh in stop_headers) or any(cleaned_line.startswith(sh) for sh in stop_headers):
                in_target_section = False
                continue
                
        if in_target_section:
            target_text.append(line)
            
    extracted = " \n ".join(target_text)
    
    if len(extracted.strip()) < 20: 
        return text.lower()
        
    return extracted.lower()

def extract_keywords(text):
    
    text = re.sub(r'[^a-zA-Z0-9\s\+#\.]', ' ', text.lower())
    words = text.split()
    
    clean_words = []
    for w in words:
        w = w.strip('.')
        if w:
            clean_words.append(w)
    keywords = set([w for w in clean_words if w not in ALL_STOP_WORDS and (len(w) > 1 or w in ['c', 'r'])])
    return keywords

def calculate_score(resume, jd):
    targeted_resume = extract_targeted_sections(resume)
    jd_keywords = extract_keywords(jd)
    resume_keywords = extract_keywords(targeted_resume)

    if not jd_keywords:
        return 0, [], []

    matched = list(jd_keywords & resume_keywords)
    missing = list(jd_keywords - resume_keywords)

    raw_score = (len(matched) / len(jd_keywords)) * 100
    

    score = round(min(raw_score * 1.4, 100), 2)

    return score, sorted(matched), sorted(missing)