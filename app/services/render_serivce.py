import logging
from typing import Dict, Any

class RendererService:
    """
    Service for rendering LaTeX equations in a user-friendly format
    """
    
    def render_equation(self, latex: str) -> Dict[str, Any]:
        """
        Render a LaTeX equation in a user-friendly format
        
        Args:
            latex: LaTeX equation to render
            
        Returns:
            Dictionary with HTML and image data for rendering
        """
        # Create a display-friendly HTML representation
        html = self._create_html_representation(latex)
        
        return {
            "html": html,
            "latex": latex
        }
    
    def _create_html_representation(self, latex: str) -> str:
        """
        Create an HTML representation of the LaTeX equation
        
        Args:
            latex: LaTeX equation
            
        Returns:
            HTML representation with MathJax
        """
        html = f"""
        <div class="math-display">
          <script type="math/tex; mode=display">{latex}</script>
        </div>
        """
        return html
