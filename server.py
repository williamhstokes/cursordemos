#!/usr/bin/env python3
"""
NFL Dashboard Python Server
Alternative to PHP for serving the dashboard and API
"""

import json
import http.server
import socketserver
import urllib.parse
from datetime import datetime
import os
import re

class NFLAPIHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        self.nfl_data = self.load_nfl_data()
        super().__init__(*args, **kwargs)
    
    def load_nfl_data(self):
        """Load NFL team data from JSON file"""
        try:
            with open('nfl_logos.json', 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading NFL data: {e}")
            return {"teams": []}
    
    def do_GET(self):
        """Handle GET requests"""
        parsed_path = urllib.parse.urlparse(self.path)
        
        # Handle API requests
        if parsed_path.path == '/api.php' or parsed_path.path == '/api':
            self.handle_api_request(parsed_path)
        else:
            # Serve static files
            super().do_GET()
    
    def handle_api_request(self, parsed_path):
        """Handle API requests"""
        query_params = urllib.parse.parse_qs(parsed_path.query)
        action = query_params.get('action', [''])[0]
        
        try:
            if action == 'getTeams':
                response = self.get_teams()
            elif action == 'getTeam':
                team_id = int(query_params.get('id', [0])[0])
                response = self.get_team(team_id)
            elif action == 'getTeamsByConference':
                conference = query_params.get('conference', [''])[0]
                response = self.get_teams_by_conference(conference)
            elif action == 'getTeamsByDivision':
                division = query_params.get('division', [''])[0]
                response = self.get_teams_by_division(division)
            elif action == 'generateLogoVariations':
                team_id = int(query_params.get('teamId', [0])[0])
                response = self.generate_logo_variations(team_id)
            elif action == 'getDesignProfile':
                response = self.get_design_profile()
            elif action == 'getLogoAnalysis':
                team_id = int(query_params.get('teamId', [0])[0])
                response = self.get_logo_analysis(team_id)
            else:
                response = self.error_response('Invalid action specified')
        except Exception as e:
            response = self.error_response(str(e))
        
        self.send_json_response(response)
    
    def send_json_response(self, data):
        """Send JSON response"""
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, indent=2).encode())
    
    def get_teams(self):
        """Get all teams"""
        # Add placeholder logos for teams without logos
        teams = self.nfl_data['teams'].copy()
        for team in teams:
            if 'logo' not in team or not team['logo']:
                team['logo'] = self.generate_placeholder_logo(team)
            team['logo_analysis'] = self.analyze_team_design_elements(team)
        
        return self.success_response({'teams': teams})
    
    def get_team(self, team_id):
        """Get specific team"""
        for team in self.nfl_data['teams']:
            if team['id'] == team_id:
                if 'logo' not in team or not team['logo']:
                    team['logo'] = self.generate_placeholder_logo(team)
                team['logo_analysis'] = self.analyze_team_design_elements(team)
                return self.success_response(team)
        
        return self.error_response('Team not found')
    
    def get_teams_by_conference(self, conference):
        """Get teams by conference"""
        teams = [team for team in self.nfl_data['teams'] 
                if team['conference'].lower() == conference.lower()]
        return self.success_response({'teams': teams})
    
    def get_teams_by_division(self, division):
        """Get teams by division"""
        teams = [team for team in self.nfl_data['teams'] 
                if team['division'].lower() == division.lower()]
        return self.success_response({'teams': teams})
    
    def generate_logo_variations(self, team_id):
        """Generate logo variations for a team"""
        team_response = self.get_team(team_id)
        if not team_response['success']:
            return team_response
        
        team = team_response['data']
        
        variations = {
            'minimalist': self.generate_minimalist_concept(team),
            'retro': self.generate_retro_concept(team),
            'modern': self.generate_modern_concept(team)
        }
        
        return self.success_response({
            'team': team,
            'variations': variations,
            'design_rationale': self.get_design_rationale(team)
        })
    
    def generate_minimalist_concept(self, team):
        """Generate minimalist design concept"""
        return {
            'style': 'Minimalist',
            'description': 'Clean, simplified design focusing on essential elements',
            'design_elements': {
                'primary_shape': self.select_primary_shape(team, 'minimalist'),
                'color_scheme': self.simplify_color_scheme(team['colors']),
                'typography': 'Sans-serif, clean letterforms',
                'visual_weight': 'Light to medium',
                'complexity': 'Low'
            },
            'concept_description': self.generate_concept_description(team, 'minimalist'),
            'svg_instructions': self.generate_svg_instructions(team, 'minimalist')
        }
    
    def generate_retro_concept(self, team):
        """Generate retro design concept"""
        return {
            'style': 'Retro Classic',
            'description': 'Vintage-inspired design with traditional NFL aesthetics',
            'design_elements': {
                'primary_shape': self.select_primary_shape(team, 'retro'),
                'color_scheme': self.enrich_color_scheme(team['colors']),
                'typography': 'Serif or slab-serif, bold letterforms',
                'visual_weight': 'Medium to heavy',
                'complexity': 'Medium'
            },
            'concept_description': self.generate_concept_description(team, 'retro'),
            'svg_instructions': self.generate_svg_instructions(team, 'retro')
        }
    
    def generate_modern_concept(self, team):
        """Generate modern design concept"""
        return {
            'style': 'Modern Dynamic',
            'description': 'Contemporary design with dynamic elements and gradients',
            'design_elements': {
                'primary_shape': self.select_primary_shape(team, 'modern'),
                'color_scheme': self.modernize_color_scheme(team['colors']),
                'typography': 'Custom sans-serif with dynamic elements',
                'visual_weight': 'Medium',
                'complexity': 'Medium to high'
            },
            'concept_description': self.generate_concept_description(team, 'modern'),
            'svg_instructions': self.generate_svg_instructions(team, 'modern')
        }
    
    def select_primary_shape(self, team, style):
        """Select primary shape based on team mascot and style"""
        mascot = team['mascot'].lower()
        
        animal_shapes = {
            'eagles': 'Stylized eagle head or spread wings',
            'falcons': 'Falcon silhouette in flight',
            'seahawks': 'Hawk head profile',
            'ravens': 'Raven silhouette',
            'cardinals': 'Cardinal head profile',
            'panthers': 'Panther head or paw print',
            'jaguars': 'Jaguar head profile',
            'bengals': 'Tiger stripes pattern',
            'bears': 'Bear head or paw',
            'lions': 'Lion head mane',
            'rams': 'Ram horns',
            'colts': 'Horseshoe',
            'broncos': 'Horse head profile',
            'dolphins': 'Dolphin jumping'
        }
        
        if mascot in animal_shapes:
            return animal_shapes[mascot]
        
        concept_shapes = {
            'patriots': 'Patriot head profile or star',
            'cowboys': 'Star',
            'steelers': 'Steel beam or hypocycloid',
            'packers': 'Letter G in circle',
            'giants': 'NY letters',
            'jets': 'Jet silhouette',
            'saints': 'Fleur-de-lis',
            'browns': 'Helmet',
            'titans': 'Flame or T logo',
            'texans': 'Bull head',
            'chiefs': 'Arrowhead',
            'raiders': 'Shield with crossed swords',
            'chargers': 'Lightning bolt',
            'bills': 'Buffalo or charging bull',
            'commanders': 'W logo or shield'
        }
        
        if mascot in concept_shapes:
            return concept_shapes[mascot]
        
        default_shapes = {
            'minimalist': 'Clean geometric circle with team initial',
            'retro': 'Classic shield shape',
            'modern': 'Dynamic angular shape'
        }
        
        return default_shapes.get(style, 'Team initial in geometric frame')
    
    def simplify_color_scheme(self, colors):
        """Simplify color scheme for minimalist design"""
        return {
            'primary': colors['primary'],
            'accent': colors['accent'],
            'usage': 'Two-color palette for maximum clarity'
        }
    
    def enrich_color_scheme(self, colors):
        """Enrich color scheme for retro design"""
        return {
            'primary': colors['primary'],
            'secondary': colors['secondary'],
            'accent': colors['accent'],
            'additional': '#8B4513',  # Classic brown for vintage feel
            'usage': 'Rich, traditional color palette'
        }
    
    def modernize_color_scheme(self, colors):
        """Modernize color scheme for contemporary design"""
        return {
            'primary': colors['primary'],
            'secondary': colors['secondary'],
            'accent': colors['accent'],
            'gradient_start': colors['primary'],
            'gradient_end': self.lighten_color(colors['primary'], 20),
            'usage': 'Dynamic gradients and modern color applications'
        }
    
    def generate_concept_description(self, team, style):
        """Generate concept description"""
        mascot = team['mascot']
        city = team['city']
        
        descriptions = {
            'minimalist': f"A clean, modern interpretation of the {mascot} identity, stripping away unnecessary details to focus on the core essence of {city}'s team spirit. Uses bold, simple shapes and limited colors for maximum impact and scalability.",
            'retro': f"Drawing inspiration from classic NFL design traditions, this vintage concept celebrates the rich history of the {mascot} with traditional shapes, classic typography, and time-honored design elements that evoke the golden era of football.",
            'modern': f"A contemporary take on the {mascot} brand, incorporating dynamic elements, subtle gradients, and modern design principles while maintaining the aggressive, powerful presence expected of an NFL franchise."
        }
        
        return descriptions.get(style, f"A unique design interpretation for the {mascot}.")
    
    def generate_svg_instructions(self, team, style):
        """Generate SVG instructions for logo creation"""
        return {
            'canvas_size': '200x200',
            'primary_element': self.select_primary_shape(team, style),
            'color_application': self.get_color_instructions(team, style),
            'typography_specs': self.get_typography_specs(style),
            'layout_guidelines': self.get_layout_guidelines(style)
        }
    
    def get_color_instructions(self, team, style):
        """Get color application instructions"""
        instructions = {
            'minimalist': {
                'background': team['colors']['primary'],
                'foreground': team['colors']['accent'],
                'accent': 'None or minimal use of secondary color'
            },
            'retro': {
                'background': 'Gradient from primary to secondary',
                'foreground': team['colors']['accent'],
                'accent': 'Traditional gold or silver highlights'
            },
            'modern': {
                'background': 'Dynamic gradient',
                'foreground': 'High contrast application',
                'accent': 'Subtle color variations and highlights'
            }
        }
        
        return instructions.get(style, instructions['minimalist'])
    
    def get_typography_specs(self, style):
        """Get typography specifications"""
        specs = {
            'minimalist': {
                'font_family': 'Clean sans-serif',
                'weight': 'Medium to bold',
                'style': 'Simple, geometric letterforms'
            },
            'retro': {
                'font_family': 'Serif or slab-serif',
                'weight': 'Bold',
                'style': 'Classic, traditional letterforms'
            },
            'modern': {
                'font_family': 'Contemporary sans-serif',
                'weight': 'Variable',
                'style': 'Dynamic, possibly custom letterforms'
            }
        }
        
        return specs.get(style, specs['minimalist'])
    
    def get_layout_guidelines(self, style):
        """Get layout guidelines"""
        guidelines = {
            'minimalist': 'Centered composition with generous white space',
            'retro': 'Traditional shield or badge layout with decorative elements',
            'modern': 'Dynamic, possibly asymmetrical composition with movement'
        }
        
        return guidelines.get(style, 'Balanced, centered composition')
    
    def get_design_profile(self):
        """Get design profile"""
        design_profile = {
            'name': 'NFL_Team_Logo_Style_Profile',
            'description': 'A design profile based on the visual elements and aesthetics of NFL team logos.',
            'overall_style': [
                'Bold',
                'Dynamic',
                'Modern with classic elements',
                'Strong and impactful',
                'Scalable for various applications'
            ],
            'common_shapes': [
                'Geometric shapes (circles, shields, stars, ovals)',
                'Stylized animal forms (birds, cats, equines)',
                'Abstract representations of objects or concepts',
                'Letterforms as central elements'
            ],
            'color_palettes': [
                'Primary and secondary colors with high contrast',
                'Limited color palettes, typically 2-4 main colors',
                'Often incorporating patriotic colors (red, white, blue)'
            ],
            'typography_style': [
                'Bold, sans-serif or slab-serif typefaces',
                'Uppercase letters common for team names or initials',
                'Custom or highly stylized letterforms',
                'Clear legibility at various sizes'
            ],
            'visual_motifs': [
                'Animal mascots (eagles, panthers, jaguars, colts, bears, falcons, seahawks)',
                'Iconic objects (stars, helmets, horseshoes, fleur-de-lis, lightning bolts)',
                'Initials or single letters representing team names',
                'Elements symbolizing location or history'
            ],
            'design_techniques': [
                'Flat design with strong outlines and clear separation of elements',
                'Subtle gradients or shadows for depth',
                'Emphasis on clean lines and simplified forms',
                'Effective use of negative space for visual impact'
            ],
            'mood_and_atmosphere': [
                'Aggressive and powerful',
                'Loyal and traditional',
                'Energetic and competitive',
                'Representing strength and determination'
            ]
        }
        
        return self.success_response(design_profile)
    
    def get_logo_analysis(self, team_id):
        """Get logo analysis for a team"""
        team_response = self.get_team(team_id)
        if not team_response['success']:
            return team_response
        
        team = team_response['data']
        
        analysis = {
            'current_logo_elements': self.analyze_current_logo(team),
            'color_psychology': self.analyze_color_psychology(team['colors']),
            'brand_positioning': self.analyze_brand_positioning(team),
            'design_opportunities': self.identify_design_opportunities(team)
        }
        
        return self.success_response(analysis)
    
    def analyze_team_design_elements(self, team):
        """Analyze team design elements"""
        return {
            'primary_motif': self.identify_primary_motif(team),
            'color_dominance': self.analyze_color_dominance(team['colors']),
            'historical_context': self.get_historical_context(team),
            'regional_influence': self.get_regional_influence(team)
        }
    
    def identify_primary_motif(self, team):
        """Identify primary motif of the team"""
        mascot = team['mascot'].lower()
        
        if mascot in ['eagles', 'falcons', 'seahawks', 'ravens', 'cardinals']:
            return 'Bird/Raptor'
        elif mascot in ['panthers', 'jaguars', 'bengals', 'bears', 'lions']:
            return 'Predator/Feline'
        elif mascot in ['colts', 'broncos', 'rams']:
            return 'Hoofed Animal'
        elif mascot in ['dolphins']:
            return 'Marine Animal'
        else:
            return 'Abstract/Conceptual'
    
    def analyze_color_dominance(self, colors):
        """Analyze color dominance"""
        primary_rgb = self.hex_to_rgb(colors['primary'])
        lightness = (primary_rgb['r'] + primary_rgb['g'] + primary_rgb['b']) / (3 * 255)
        
        if lightness < 0.3:
            return 'Dark-dominant (Strong, Authoritative)'
        elif lightness > 0.7:
            return 'Light-dominant (Clean, Modern)'
        else:
            return 'Balanced (Versatile, Dynamic)'
    
    def get_historical_context(self, team):
        """Get historical context"""
        founded = team['founded']
        
        if founded < 1950:
            return 'Original NFL era - Traditional design heritage'
        elif founded < 1970:
            return 'Expansion era - Classic modernization period'
        elif founded < 1995:
            return 'Modern expansion - Contemporary design influence'
        else:
            return 'Recent expansion - Modern brand development'
    
    def get_regional_influence(self, team):
        """Get regional influence"""
        city = team['city'].lower()
        
        regional_influences = {
            'new england': 'Colonial American heritage',
            'new orleans': 'French Creole culture',
            'green bay': 'Industrial Midwest tradition',
            'san francisco': 'California innovation culture',
            'seattle': 'Pacific Northwest nature themes',
            'miami': 'Tropical, vibrant aesthetics',
            'denver': 'Mountain West ruggedness',
            'dallas': 'Texas pride and scale',
            'las vegas': 'Entertainment and glamour'
        }
        
        for region, influence in regional_influences.items():
            if region in city:
                return influence
        
        return 'General American sports culture'
    
    def analyze_current_logo(self, team):
        """Analyze current logo elements"""
        return {
            'primary_element': self.select_primary_shape(team, 'current'),
            'color_usage': f"Primary: {team['colors']['primary']}, Secondary: {team['colors']['secondary']}",
            'style_era': self.get_historical_context(team),
            'complexity_level': 'Medium'
        }
    
    def analyze_color_psychology(self, colors):
        """Analyze color psychology"""
        primary_rgb = self.hex_to_rgb(colors['primary'])
        
        if self.is_red(primary_rgb):
            return 'Red conveys power, aggression, and passion'
        elif self.is_blue(primary_rgb):
            return 'Blue represents trust, stability, and professionalism'
        elif self.is_green(primary_rgb):
            return 'Green symbolizes growth, nature, and freshness'
        elif self.is_yellow(primary_rgb):
            return 'Yellow/Gold represents excellence, energy, and optimism'
        else:
            return 'Unique color choice for distinctive brand identity'
    
    def analyze_brand_positioning(self, team):
        """Analyze brand positioning"""
        return {
            'market_position': f"{team['conference']} {team['division']} team",
            'brand_personality': 'Strong, competitive, regional pride',
            'target_audience': 'Local fanbase and national NFL audience',
            'differentiation': f"Unique {team['mascot']} identity in {team['city']}"
        }
    
    def identify_design_opportunities(self, team):
        """Identify design opportunities"""
        return [
            'Modernize typography for better digital applications',
            'Simplify complex elements for better scalability',
            'Enhance color contrast for accessibility',
            'Create responsive logo variations for different contexts'
        ]
    
    def get_design_rationale(self, team):
        """Get design rationale"""
        return {
            'team_identity': f"The {team['name']} represent {team['city']} with a {team['mascot']} identity",
            'color_significance': self.analyze_color_psychology(team['colors']),
            'historical_context': self.get_historical_context(team),
            'design_philosophy': ['Aggressive and powerful', 'Loyal and traditional', 'Energetic and competitive']
        }
    
    def generate_placeholder_logo(self, team):
        """Generate placeholder logo URL"""
        primary_color = team['colors']['primary'].lstrip('#')
        accent_color = team['colors']['accent'].lstrip('#')
        initial = team['mascot'][0]
        
        return f"https://via.placeholder.com/200x200/{primary_color}/{accent_color}?text={initial}"
    
    # Utility functions
    def hex_to_rgb(self, hex_color):
        """Convert hex to RGB"""
        hex_color = hex_color.lstrip('#')
        return {
            'r': int(hex_color[0:2], 16),
            'g': int(hex_color[2:4], 16),
            'b': int(hex_color[4:6], 16)
        }
    
    def lighten_color(self, hex_color, percent):
        """Lighten a hex color by percentage"""
        rgb = self.hex_to_rgb(hex_color)
        
        rgb['r'] = min(255, int(rgb['r'] + (percent * 255 / 100)))
        rgb['g'] = min(255, int(rgb['g'] + (percent * 255 / 100)))
        rgb['b'] = min(255, int(rgb['b'] + (percent * 255 / 100)))
        
        return f"#{rgb['r']:02x}{rgb['g']:02x}{rgb['b']:02x}"
    
    def is_red(self, rgb):
        """Check if color is predominantly red"""
        return rgb['r'] > rgb['g'] and rgb['r'] > rgb['b'] and rgb['r'] > 150
    
    def is_blue(self, rgb):
        """Check if color is predominantly blue"""
        return rgb['b'] > rgb['r'] and rgb['b'] > rgb['g'] and rgb['b'] > 150
    
    def is_green(self, rgb):
        """Check if color is predominantly green"""
        return rgb['g'] > rgb['r'] and rgb['g'] > rgb['b'] and rgb['g'] > 150
    
    def is_yellow(self, rgb):
        """Check if color is predominantly yellow"""
        return rgb['r'] > 200 and rgb['g'] > 200 and rgb['b'] < 100
    
    def success_response(self, data):
        """Create success response"""
        return {
            'success': True,
            'data': data,
            'timestamp': datetime.now().isoformat()
        }
    
    def error_response(self, message):
        """Create error response"""
        return {
            'success': False,
            'error': message,
            'timestamp': datetime.now().isoformat()
        }

def start_server(port=8000):
    """Start the NFL dashboard server"""
    handler = NFLAPIHandler
    
    with socketserver.TCPServer(("", port), handler) as httpd:
        print(f"🏈 NFL Dashboard Server running at http://localhost:{port}")
        print("📊 API endpoints available:")
        print("  - /api?action=getTeams")
        print("  - /api?action=getTeam&id={teamId}")
        print("  - /api?action=generateLogoVariations&teamId={id}")
        print("  - /api?action=getDesignProfile")
        print("\n✨ Open http://localhost:8000 in your browser to view the dashboard")
        print("🛑 Press Ctrl+C to stop the server\n")
        
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Server stopped")
            httpd.shutdown()

if __name__ == "__main__":
    start_server()