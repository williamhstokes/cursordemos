<?php
/**
 * NFL Team Logo Dashboard API
 * Handles data operations and logo generation logic
 */

header('Content-Type: application/json');
header('Access-Control-Allow-Origin: *');
header('Access-Control-Allow-Methods: GET, POST, OPTIONS');
header('Access-Control-Allow-Headers: Content-Type');

// Handle preflight requests
if ($_SERVER['REQUEST_METHOD'] === 'OPTIONS') {
    http_response_code(200);
    exit();
}

class NFLTeamAPI {
    private $dataFile;
    private $designProfile;
    
    public function __construct() {
        $this->dataFile = __DIR__ . '/nfl_logos.json';
        $this->designProfile = [
            'name' => 'NFL_Team_Logo_Style_Profile',
            'description' => 'A design profile based on the visual elements and aesthetics of NFL team logos.',
            'overall_style' => [
                'Bold',
                'Dynamic',
                'Modern with classic elements',
                'Strong and impactful',
                'Scalable for various applications'
            ],
            'common_shapes' => [
                'Geometric shapes (circles, shields, stars, ovals)',
                'Stylized animal forms (birds, cats, equines)',
                'Abstract representations of objects or concepts',
                'Letterforms as central elements'
            ],
            'color_palettes' => [
                'Primary and secondary colors with high contrast',
                'Limited color palettes, typically 2-4 main colors',
                'Often incorporating patriotic colors (red, white, blue)'
            ],
            'typography_style' => [
                'Bold, sans-serif or slab-serif typefaces',
                'Uppercase letters common for team names or initials',
                'Custom or highly stylized letterforms',
                'Clear legibility at various sizes'
            ],
            'visual_motifs' => [
                'Animal mascots (eagles, panthers, jaguars, colts, bears, falcons, seahawks)',
                'Iconic objects (stars, helmets, horseshoes, fleur-de-lis, lightning bolts)',
                'Initials or single letters representing team names',
                'Elements symbolizing location or history'
            ],
            'design_techniques' => [
                'Flat design with strong outlines and clear separation of elements',
                'Subtle gradients or shadows for depth',
                'Emphasis on clean lines and simplified forms',
                'Effective use of negative space for visual impact'
            ],
            'mood_and_atmosphere' => [
                'Aggressive and powerful',
                'Loyal and traditional',
                'Energetic and competitive',
                'Representing strength and determination'
            ]
        ];
    }
    
    public function handleRequest() {
        $action = $_GET['action'] ?? '';
        
        try {
            switch ($action) {
                case 'getTeams':
                    return $this->getTeams();
                    
                case 'getTeam':
                    $teamId = intval($_GET['id'] ?? 0);
                    return $this->getTeam($teamId);
                    
                case 'getTeamsByConference':
                    $conference = $_GET['conference'] ?? '';
                    return $this->getTeamsByConference($conference);
                    
                case 'getTeamsByDivision':
                    $division = $_GET['division'] ?? '';
                    return $this->getTeamsByDivision($division);
                    
                case 'generateLogoVariations':
                    $teamId = intval($_GET['teamId'] ?? 0);
                    return $this->generateLogoVariations($teamId);
                    
                case 'getDesignProfile':
                    return $this->getDesignProfile();
                    
                case 'getLogoAnalysis':
                    $teamId = intval($_GET['teamId'] ?? 0);
                    return $this->getLogoAnalysis($teamId);
                    
                default:
                    throw new Exception('Invalid action specified');
            }
        } catch (Exception $e) {
            return $this->errorResponse($e->getMessage());
        }
    }
    
    private function getTeams() {
        if (!file_exists($this->dataFile)) {
            throw new Exception('Teams data file not found');
        }
        
        $jsonData = file_get_contents($this->dataFile);
        $data = json_decode($jsonData, true);
        
        if (json_last_error() !== JSON_ERROR_NONE) {
            throw new Exception('Invalid JSON data');
        }
        
        // Add generated logo URLs for teams without logos
        foreach ($data['teams'] as &$team) {
            if (!isset($team['logo']) || empty($team['logo'])) {
                $team['logo'] = $this->generatePlaceholderLogo($team);
            }
            
            // Add additional metadata
            $team['logo_analysis'] = $this->analyzeTeamDesignElements($team);
        }
        
        return $this->successResponse($data);
    }
    
    private function getTeam($teamId) {
        $teamsResponse = $this->getTeams();
        $teams = $teamsResponse['data']['teams'];
        
        foreach ($teams as $team) {
            if ($team['id'] === $teamId) {
                return $this->successResponse($team);
            }
        }
        
        throw new Exception('Team not found');
    }
    
    private function getTeamsByConference($conference) {
        $teamsResponse = $this->getTeams();
        $teams = $teamsResponse['data']['teams'];
        
        $filteredTeams = array_filter($teams, function($team) use ($conference) {
            return strcasecmp($team['conference'], $conference) === 0;
        });
        
        return $this->successResponse(['teams' => array_values($filteredTeams)]);
    }
    
    private function getTeamsByDivision($division) {
        $teamsResponse = $this->getTeams();
        $teams = $teamsResponse['data']['teams'];
        
        $filteredTeams = array_filter($teams, function($team) use ($division) {
            return strcasecmp($team['division'], $division) === 0;
        });
        
        return $this->successResponse(['teams' => array_values($filteredTeams)]);
    }
    
    private function generateLogoVariations($teamId) {
        $teamResponse = $this->getTeam($teamId);
        $team = $teamResponse['data'];
        
        $variations = [
            'minimalist' => $this->generateMinimalistConcept($team),
            'retro' => $this->generateRetroConcept($team),
            'modern' => $this->generateModernConcept($team)
        ];
        
        return $this->successResponse([
            'team' => $team,
            'variations' => $variations,
            'design_rationale' => $this->getDesignRationale($team)
        ]);
    }
    
    private function generateMinimalistConcept($team) {
        return [
            'style' => 'Minimalist',
            'description' => 'Clean, simplified design focusing on essential elements',
            'design_elements' => [
                'primary_shape' => $this->selectPrimaryShape($team, 'minimalist'),
                'color_scheme' => $this->simplifyColorScheme($team['colors']),
                'typography' => 'Sans-serif, clean letterforms',
                'visual_weight' => 'Light to medium',
                'complexity' => 'Low'
            ],
            'concept_description' => $this->generateConceptDescription($team, 'minimalist'),
            'svg_instructions' => $this->generateSVGInstructions($team, 'minimalist')
        ];
    }
    
    private function generateRetroConcept($team) {
        return [
            'style' => 'Retro Classic',
            'description' => 'Vintage-inspired design with traditional NFL aesthetics',
            'design_elements' => [
                'primary_shape' => $this->selectPrimaryShape($team, 'retro'),
                'color_scheme' => $this->enrichColorScheme($team['colors']),
                'typography' => 'Serif or slab-serif, bold letterforms',
                'visual_weight' => 'Medium to heavy',
                'complexity' => 'Medium'
            ],
            'concept_description' => $this->generateConceptDescription($team, 'retro'),
            'svg_instructions' => $this->generateSVGInstructions($team, 'retro')
        ];
    }
    
    private function generateModernConcept($team) {
        return [
            'style' => 'Modern Dynamic',
            'description' => 'Contemporary design with dynamic elements and gradients',
            'design_elements' => [
                'primary_shape' => $this->selectPrimaryShape($team, 'modern'),
                'color_scheme' => $this->modernizeColorScheme($team['colors']),
                'typography' => 'Custom sans-serif with dynamic elements',
                'visual_weight' => 'Medium',
                'complexity' => 'Medium to high'
            ],
            'concept_description' => $this->generateConceptDescription($team, 'modern'),
            'svg_instructions' => $this->generateSVGInstructions($team, 'modern')
        ];
    }
    
    private function selectPrimaryShape($team, $style) {
        $mascot = strtolower($team['mascot']);
        
        // Animal-based teams
        $animalShapes = [
            'eagles' => 'Stylized eagle head or spread wings',
            'falcons' => 'Falcon silhouette in flight',
            'seahawks' => 'Hawk head profile',
            'ravens' => 'Raven silhouette',
            'cardinals' => 'Cardinal head profile',
            'panthers' => 'Panther head or paw print',
            'jaguars' => 'Jaguar head profile',
            'bengals' => 'Tiger stripes pattern',
            'bears' => 'Bear head or paw',
            'lions' => 'Lion head mane',
            'rams' => 'Ram horns',
            'colts' => 'Horseshoe',
            'broncos' => 'Horse head profile',
            'dolphins' => 'Dolphin jumping'
        ];
        
        if (isset($animalShapes[$mascot])) {
            return $animalShapes[$mascot];
        }
        
        // Location or concept-based teams
        $conceptShapes = [
            'patriots' => 'Patriot head profile or star',
            'cowboys' => 'Star',
            'steelers' => 'Steel beam or hypocycloid',
            'packers' => 'Letter G in circle',
            'giants' => 'NY letters',
            'jets' => 'Jet silhouette',
            'saints' => 'Fleur-de-lis',
            'browns' => 'Helmet',
            'titans' => 'Flame or T logo',
            'texans' => 'Bull head',
            'chiefs' => 'Arrowhead',
            'raiders' => 'Shield with crossed swords',
            'chargers' => 'Lightning bolt',
            'bills' => 'Buffalo or charging bull',
            'commanders' => 'W logo or shield'
        ];
        
        if (isset($conceptShapes[$mascot])) {
            return $conceptShapes[$mascot];
        }
        
        // Default shapes based on style
        $defaultShapes = [
            'minimalist' => 'Clean geometric circle with team initial',
            'retro' => 'Classic shield shape',
            'modern' => 'Dynamic angular shape'
        ];
        
        return $defaultShapes[$style] ?? 'Team initial in geometric frame';
    }
    
    private function simplifyColorScheme($colors) {
        return [
            'primary' => $colors['primary'],
            'accent' => $colors['accent'],
            'usage' => 'Two-color palette for maximum clarity'
        ];
    }
    
    private function enrichColorScheme($colors) {
        return [
            'primary' => $colors['primary'],
            'secondary' => $colors['secondary'],
            'accent' => $colors['accent'],
            'additional' => '#8B4513', // Classic brown for vintage feel
            'usage' => 'Rich, traditional color palette'
        ];
    }
    
    private function modernizeColorScheme($colors) {
        return [
            'primary' => $colors['primary'],
            'secondary' => $colors['secondary'],
            'accent' => $colors['accent'],
            'gradient_start' => $colors['primary'],
            'gradient_end' => $this->lightenColor($colors['primary'], 20),
            'usage' => 'Dynamic gradients and modern color applications'
        ];
    }
    
    private function generateConceptDescription($team, $style) {
        $mascot = $team['mascot'];
        $city = $team['city'];
        
        $descriptions = [
            'minimalist' => "A clean, modern interpretation of the {$mascot} identity, stripping away unnecessary details to focus on the core essence of {$city}'s team spirit. Uses bold, simple shapes and limited colors for maximum impact and scalability.",
            
            'retro' => "Drawing inspiration from classic NFL design traditions, this vintage concept celebrates the rich history of the {$mascot} with traditional shapes, classic typography, and time-honored design elements that evoke the golden era of football.",
            
            'modern' => "A contemporary take on the {$mascot} brand, incorporating dynamic elements, subtle gradients, and modern design principles while maintaining the aggressive, powerful presence expected of an NFL franchise."
        ];
        
        return $descriptions[$style] ?? "A unique design interpretation for the {$mascot}.";
    }
    
    private function generateSVGInstructions($team, $style) {
        return [
            'canvas_size' => '200x200',
            'primary_element' => $this->selectPrimaryShape($team, $style),
            'color_application' => $this->getColorInstructions($team, $style),
            'typography_specs' => $this->getTypographySpecs($style),
            'layout_guidelines' => $this->getLayoutGuidelines($style)
        ];
    }
    
    private function getColorInstructions($team, $style) {
        $instructions = [
            'minimalist' => [
                'background' => $team['colors']['primary'],
                'foreground' => $team['colors']['accent'],
                'accent' => 'None or minimal use of secondary color'
            ],
            'retro' => [
                'background' => 'Gradient from primary to secondary',
                'foreground' => $team['colors']['accent'],
                'accent' => 'Traditional gold or silver highlights'
            ],
            'modern' => [
                'background' => 'Dynamic gradient',
                'foreground' => 'High contrast application',
                'accent' => 'Subtle color variations and highlights'
            ]
        ];
        
        return $instructions[$style] ?? $instructions['minimalist'];
    }
    
    private function getTypographySpecs($style) {
        $specs = [
            'minimalist' => [
                'font_family' => 'Clean sans-serif',
                'weight' => 'Medium to bold',
                'style' => 'Simple, geometric letterforms'
            ],
            'retro' => [
                'font_family' => 'Serif or slab-serif',
                'weight' => 'Bold',
                'style' => 'Classic, traditional letterforms'
            ],
            'modern' => [
                'font_family' => 'Contemporary sans-serif',
                'weight' => 'Variable',
                'style' => 'Dynamic, possibly custom letterforms'
            ]
        ];
        
        return $specs[$style] ?? $specs['minimalist'];
    }
    
    private function getLayoutGuidelines($style) {
        $guidelines = [
            'minimalist' => 'Centered composition with generous white space',
            'retro' => 'Traditional shield or badge layout with decorative elements',
            'modern' => 'Dynamic, possibly asymmetrical composition with movement'
        ];
        
        return $guidelines[$style] ?? 'Balanced, centered composition';
    }
    
    private function getDesignProfile() {
        return $this->successResponse($this->designProfile);
    }
    
    private function getLogoAnalysis($teamId) {
        $teamResponse = $this->getTeam($teamId);
        $team = $teamResponse['data'];
        
        $analysis = [
            'current_logo_elements' => $this->analyzeCurrentLogo($team),
            'color_psychology' => $this->analyzeColorPsychology($team['colors']),
            'brand_positioning' => $this->analyzeBrandPositioning($team),
            'design_opportunities' => $this->identifyDesignOpportunities($team)
        ];
        
        return $this->successResponse($analysis);
    }
    
    private function analyzeTeamDesignElements($team) {
        return [
            'primary_motif' => $this->identifyPrimaryMotif($team),
            'color_dominance' => $this->analyzeColorDominance($team['colors']),
            'historical_context' => $this->getHistoricalContext($team),
            'regional_influence' => $this->getRegionalInfluence($team)
        ];
    }
    
    private function identifyPrimaryMotif($team) {
        $mascot = strtolower($team['mascot']);
        
        if (in_array($mascot, ['eagles', 'falcons', 'seahawks', 'ravens', 'cardinals'])) {
            return 'Bird/Raptor';
        } elseif (in_array($mascot, ['panthers', 'jaguars', 'bengals', 'bears', 'lions'])) {
            return 'Predator/Feline';
        } elseif (in_array($mascot, ['colts', 'broncos', 'rams'])) {
            return 'Hoofed Animal';
        } elseif (in_array($mascot, ['dolphins'])) {
            return 'Marine Animal';
        } else {
            return 'Abstract/Conceptual';
        }
    }
    
    private function analyzeColorDominance($colors) {
        $primary = $this->hexToRgb($colors['primary']);
        $hsl = $this->rgbToHsl($primary['r'], $primary['g'], $primary['b']);
        
        if ($hsl['l'] < 0.3) {
            return 'Dark-dominant (Strong, Authoritative)';
        } elseif ($hsl['l'] > 0.7) {
            return 'Light-dominant (Clean, Modern)';
        } else {
            return 'Balanced (Versatile, Dynamic)';
        }
    }
    
    private function getHistoricalContext($team) {
        $founded = $team['founded'];
        
        if ($founded < 1950) {
            return 'Original NFL era - Traditional design heritage';
        } elseif ($founded < 1970) {
            return 'Expansion era - Classic modernization period';
        } elseif ($founded < 1995) {
            return 'Modern expansion - Contemporary design influence';
        } else {
            return 'Recent expansion - Modern brand development';
        }
    }
    
    private function getRegionalInfluence($team) {
        $city = strtolower($team['city']);
        
        $regional_influences = [
            'new england' => 'Colonial American heritage',
            'new orleans' => 'French Creole culture',
            'green bay' => 'Industrial Midwest tradition',
            'san francisco' => 'California innovation culture',
            'seattle' => 'Pacific Northwest nature themes',
            'miami' => 'Tropical, vibrant aesthetics',
            'denver' => 'Mountain West ruggedness',
            'dallas' => 'Texas pride and scale',
            'las vegas' => 'Entertainment and glamour'
        ];
        
        foreach ($regional_influences as $region => $influence) {
            if (strpos($city, $region) !== false) {
                return $influence;
            }
        }
        
        return 'General American sports culture';
    }
    
    private function generatePlaceholderLogo($team) {
        $primaryColor = urlencode(ltrim($team['colors']['primary'], '#'));
        $accentColor = urlencode(ltrim($team['colors']['accent'], '#'));
        $initial = urlencode(substr($team['mascot'], 0, 1));
        
        return "https://via.placeholder.com/200x200/{$primaryColor}/{$accentColor}?text={$initial}";
    }
    
    private function getDesignRationale($team) {
        return [
            'team_identity' => "The {$team['name']} represent {$team['city']} with a {$team['mascot']} identity",
            'color_significance' => $this->explainColorChoices($team['colors']),
            'historical_context' => $this->getHistoricalContext($team),
            'design_philosophy' => $this->designProfile['mood_and_atmosphere']
        ];
    }
    
    private function explainColorChoices($colors) {
        $explanations = [];
        
        // Analyze primary color
        $primary = $this->hexToRgb($colors['primary']);
        if ($this->isRed($primary)) {
            $explanations[] = 'Red conveys power, aggression, and passion';
        } elseif ($this->isBlue($primary)) {
            $explanations[] = 'Blue represents trust, stability, and professionalism';
        } elseif ($this->isGreen($primary)) {
            $explanations[] = 'Green symbolizes growth, nature, and freshness';
        } elseif ($this->isYellow($primary)) {
            $explanations[] = 'Yellow/Gold represents excellence, energy, and optimism';
        } else {
            $explanations[] = 'Unique color choice for distinctive brand identity';
        }
        
        return implode('. ', $explanations);
    }
    
    // Utility functions
    private function hexToRgb($hex) {
        $hex = ltrim($hex, '#');
        return [
            'r' => hexdec(substr($hex, 0, 2)),
            'g' => hexdec(substr($hex, 2, 2)),
            'b' => hexdec(substr($hex, 4, 2))
        ];
    }
    
    private function rgbToHsl($r, $g, $b) {
        $r /= 255;
        $g /= 255;
        $b /= 255;
        
        $max = max($r, $g, $b);
        $min = min($r, $g, $b);
        $h = $s = $l = ($max + $min) / 2;
        
        if ($max == $min) {
            $h = $s = 0;
        } else {
            $d = $max - $min;
            $s = $l > 0.5 ? $d / (2 - $max - $min) : $d / ($max + $min);
            
            switch ($max) {
                case $r: $h = ($g - $b) / $d + ($g < $b ? 6 : 0); break;
                case $g: $h = ($b - $r) / $d + 2; break;
                case $b: $h = ($r - $g) / $d + 4; break;
            }
            $h /= 6;
        }
        
        return ['h' => $h, 's' => $s, 'l' => $l];
    }
    
    private function lightenColor($hex, $percent) {
        $rgb = $this->hexToRgb($hex);
        
        $rgb['r'] = min(255, $rgb['r'] + ($percent * 255 / 100));
        $rgb['g'] = min(255, $rgb['g'] + ($percent * 255 / 100));
        $rgb['b'] = min(255, $rgb['b'] + ($percent * 255 / 100));
        
        return sprintf('#%02x%02x%02x', $rgb['r'], $rgb['g'], $rgb['b']);
    }
    
    private function isRed($rgb) {
        return $rgb['r'] > $rgb['g'] && $rgb['r'] > $rgb['b'] && $rgb['r'] > 150;
    }
    
    private function isBlue($rgb) {
        return $rgb['b'] > $rgb['r'] && $rgb['b'] > $rgb['g'] && $rgb['b'] > 150;
    }
    
    private function isGreen($rgb) {
        return $rgb['g'] > $rgb['r'] && $rgb['g'] > $rgb['b'] && $rgb['g'] > 150;
    }
    
    private function isYellow($rgb) {
        return $rgb['r'] > 200 && $rgb['g'] > 200 && $rgb['b'] < 100;
    }
    
    private function successResponse($data) {
        return [
            'success' => true,
            'data' => $data,
            'timestamp' => date('c')
        ];
    }
    
    private function errorResponse($message) {
        http_response_code(400);
        return [
            'success' => false,
            'error' => $message,
            'timestamp' => date('c')
        ];
    }
}

// Handle the request
$api = new NFLTeamAPI();
$response = $api->handleRequest();

echo json_encode($response, JSON_PRETTY_PRINT);
?>