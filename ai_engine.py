"""
AI Engine for RedAI Pen Testing Tool
Handles AI model integration for exploit generation and selection
"""

import os
import json
from typing import List, Dict, Optional
from config import (
    AI_PROVIDER, OPENAI_API_KEY, ANTHROPIC_API_KEY, MODEL_NAME,
    LOCAL_MODEL_PATH, LOCAL_MODEL_TYPE
)

class AIEngine:
    """AI engine for generating and selecting exploits"""
    
    def __init__(self):
        self.provider = AI_PROVIDER
        self.model_name = MODEL_NAME
        self._init_client()
    
    def _init_client(self):
        """Initialize AI client based on provider"""
        if self.provider == "openai":
            try:
                from openai import OpenAI
                if not OPENAI_API_KEY:
                    raise ValueError("OPENAI_API_KEY not set in environment")
                self.client = OpenAI(api_key=OPENAI_API_KEY)
            except ImportError:
                raise ImportError("openai package not installed. Run: pip install openai")
        elif self.provider == "anthropic":
            try:
                import anthropic
                if not ANTHROPIC_API_KEY:
                    raise ValueError("ANTHROPIC_API_KEY not set in environment")
                self.client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
            except ImportError:
                raise ImportError("anthropic package not installed. Run: pip install anthropic")
        else:
            # Local model support (placeholder for future implementation)
            self.client = None
            print("Warning: Local model support not yet implemented")
    
    def analyze_target(self, user_prompt: str, available_exploits: List[Dict]) -> Dict:
        """
        Analyze user prompt and select best exploit or determine if new one needed
        
        Returns:
            Dict with 'action' ('use_existing' or 'generate_new'), 
            'exploit_id' (if use_existing), or 'generation_prompt' (if generate_new)
        """
        if self.provider == "openai":
            return self._analyze_with_openai(user_prompt, available_exploits)
        elif self.provider == "anthropic":
            return self._analyze_with_anthropic(user_prompt, available_exploits)
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")
    
    def _analyze_with_openai(self, user_prompt: str, available_exploits: List[Dict]) -> Dict:
        """Analyze using OpenAI API"""
        exploits_summary = self._format_exploits_for_ai(available_exploits)
        
        system_prompt = """You are an expert penetration tester AI assistant. Your role is to:
1. Analyze user requests for penetration testing goals
2. Match them with known exploits from the database
3. If no suitable exploit exists, determine what new exploit needs to be generated

Respond in JSON format with:
- "action": either "use_existing" or "generate_new"
- "exploit_id": (if use_existing) the ID of the best matching exploit
- "reasoning": brief explanation of your decision
- "generation_prompt": (if generate_new) detailed prompt for generating new exploit"""
        
        user_message = f"""User Goal: {user_prompt}

Available Exploits:
{exploits_summary}

Analyze this request and determine the best course of action."""
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    
    def _analyze_with_anthropic(self, user_prompt: str, available_exploits: List[Dict]) -> Dict:
        """Analyze using Anthropic API"""
        exploits_summary = self._format_exploits_for_ai(available_exploits)
        
        system_prompt = """You are an expert penetration tester AI assistant. Your role is to:
1. Analyze user requests for penetration testing goals
2. Match them with known exploits from the database
3. If no suitable exploit exists, determine what new exploit needs to be generated

Respond in JSON format with:
- "action": either "use_existing" or "generate_new"
- "exploit_id": (if use_existing) the ID of the best matching exploit
- "reasoning": brief explanation of your decision
- "generation_prompt": (if generate_new) detailed prompt for generating new exploit"""
        
        user_message = f"""User Goal: {user_prompt}

Available Exploits:
{exploits_summary}

Analyze this request and determine the best course of action."""
        
        response = self.client.messages.create(
            model=self.model_name if self.model_name.startswith("claude") else "claude-3-haiku-20240307",
            max_tokens=1024,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        
        result = json.loads(response.content[0].text)
        return result
    
    def generate_new_exploit(self, target_description: str, goal: str) -> Dict:
        """
        Generate a new exploit based on target description and goal
        
        Returns:
            Dict with exploit details: name, description, target_type, 
            target_component, method_summary, steps, tools_required
        """
        if self.provider == "openai":
            return self._generate_with_openai(target_description, goal)
        elif self.provider == "anthropic":
            return self._generate_with_anthropic(target_description, goal)
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")
    
    def _generate_with_openai(self, target_description: str, goal: str) -> Dict:
        """Generate exploit using OpenAI API"""
        system_prompt = """You are an expert penetration tester. Generate detailed exploit methods
for educational penetration testing purposes. Always prioritize ethical considerations.

Respond in JSON format with:
- "name": short descriptive name
- "description": detailed description
- "target_type": type of target (e.g., "web_app", "network", "api", "iot")
- "target_component": specific component (e.g., "authentication", "file_upload")
- "method_summary": brief summary of the method
- "difficulty": "easy", "medium", or "hard"
- "tools_required": array of tool names
- "steps": array of step objects, each with:
  - "description": what this step does
  - "command": command to execute (if applicable)
  - "expected_output": what to expect"""
        
        user_message = f"""Generate a penetration testing exploit method for:

Target: {target_description}
Goal: {goal}

Create a detailed, step-by-step method that can be automated."""
        
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_message}
            ],
            response_format={"type": "json_object"},
            temperature=0.7
        )
        
        result = json.loads(response.choices[0].message.content)
        return result
    
    def _generate_with_anthropic(self, target_description: str, goal: str) -> Dict:
        """Generate exploit using Anthropic API"""
        system_prompt = """You are an expert penetration tester. Generate detailed exploit methods
for educational penetration testing purposes. Always prioritize ethical considerations.

Respond in JSON format with:
- "name": short descriptive name
- "description": detailed description
- "target_type": type of target (e.g., "web_app", "network", "api", "iot")
- "target_component": specific component (e.g., "authentication", "file_upload")
- "method_summary": brief summary of the method
- "difficulty": "easy", "medium", or "hard"
- "tools_required": array of tool names
- "steps": array of step objects, each with:
  - "description": what this step does
  - "command": command to execute (if applicable)
  - "expected_output": what to expect"""
        
        user_message = f"""Generate a penetration testing exploit method for:

Target: {target_description}
Goal: {goal}

Create a detailed, step-by-step method that can be automated."""
        
        response = self.client.messages.create(
            model="claude-3-haiku-20240307",
            max_tokens=2048,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}]
        )
        
        result = json.loads(response.content[0].text)
        return result
    
    def _format_exploits_for_ai(self, exploits: List[Dict]) -> str:
        """Format exploits list for AI consumption"""
        if not exploits:
            return "No exploits available in database."
        
        formatted = []
        for exp in exploits:
            formatted.append(
                f"ID: {exp['id']}\n"
                f"Name: {exp['name']}\n"
                f"Target: {exp['target_component']} ({exp['target_type']})\n"
                f"Description: {exp['description']}\n"
                f"Method: {exp['method_summary']}\n"
                f"Success Rate: {exp['success_rate']}\n"
                f"Difficulty: {exp['difficulty']}\n"
            )
        
        return "\n---\n".join(formatted)







