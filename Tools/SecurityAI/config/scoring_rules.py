class ScoringRules:
    """评分规则定义"""
    
    @staticmethod
    def get_malware_score_description(score):
        """获取恶意软件评分描述"""
        if score == 0:
            return "No malicious intent"
        elif 0 < score <= 0.25:
            return "Low possibility of malicious intent"
        elif 0.25 < score <= 0.5:
            return "Possibly malicious behavior"
        elif 0.5 < score <= 0.75:
            return "Likely malicious behavior"
        else:
            return "High probability of malicious behavior"
    
    @staticmethod
    def get_security_risk_description(score):
        """获取安全风险评分描述"""
        if score <= 0.25:
            return "No significant threat"
        elif 0.25 < score <= 0.5:
            return "Security warning, no immediate danger"
        elif 0.5 < score <= 0.75:
            return "Security alert should be reviewed"
        else:
            return "Extremely dangerous"
    
    @staticmethod
    def is_package_malicious(malware_score, security_risk_score):
        """判断包是否恶意"""
        return malware_score > 0.5