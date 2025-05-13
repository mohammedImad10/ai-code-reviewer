class Reviewer:
    def __init__(self):
        pass

    def construct_prompt(self, file_content):
        prompt = (
            "You are an expert code reviewer. Please review the following code and provide detailed, actionable feedback. "
            "Focus on:"
            "\n- Code quality and best practices"
            "\n- Potential bugs or edge cases"
            "\n- Performance issues"
            "\n- Security vulnerabilities"
            "\n- Readability and maintainability"
            "\n\nFormat your response as a list of specific suggestions, each on a new line. "
            "Be concise but thorough. Provide code examples where helpful.\n\n"
            f"```\n{file_content}\n```\n"
        )
        return prompt

    def parse_response(self, response):
        """Parse the LLM response into a list of suggestions."""
        if hasattr(response, 'output') and hasattr(response.output, 'text'):
            # New Together.ai API response format
            content = response.output.text
        elif hasattr(response, 'choices'):
            # Old Together.ai API response format
            content = response.choices[0].message.content
        elif isinstance(response, dict):
            # Handle dictionary response format
            if 'output' in response and 'text' in response['output']:
                content = response['output']['text']
            else:
                content = response.get('choices', [{}])[0].get('message', {}).get('content', '')
        else:
            # Fallback for string or other formats
            content = str(response)
        
        # Clean up the response
        lines = content.split('\n')
        suggestions = []
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('```'):
                suggestions.append(line)
        
        return suggestions
