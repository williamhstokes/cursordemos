// NFL Dashboard JavaScript
class NFLLogoDashboard {
    constructor() {
        this.teams = [];
        this.filteredTeams = [];
        this.selectedTeam = null;
        this.designProfile = {
            name: "NFL_Team_Logo_Style_Profile",
            description: "A design profile based on the visual elements and aesthetics of NFL team logos.",
            overall_style: [
                "Bold",
                "Dynamic", 
                "Modern with classic elements",
                "Strong and impactful",
                "Scalable for various applications"
            ],
            common_shapes: [
                "Geometric shapes (circles, shields, stars, ovals)",
                "Stylized animal forms (birds, cats, equines)",
                "Abstract representations of objects or concepts",
                "Letterforms as central elements"
            ],
            color_palettes: [
                "Primary and secondary colors with high contrast",
                "Limited color palettes, typically 2-4 main colors",
                "Often incorporating patriotic colors (red, white, blue)"
            ],
            typography_style: [
                "Bold, sans-serif or slab-serif typefaces",
                "Uppercase letters common for team names or initials",
                "Custom or highly stylized letterforms",
                "Clear legibility at various sizes"
            ],
            visual_motifs: [
                "Animal mascots (eagles, panthers, jaguars, colts, bears, falcons, seahawks)",
                "Iconic objects (stars, helmets, horseshoes, fleur-de-lis, lightning bolts)",
                "Initials or single letters representing team names",
                "Elements symbolizing location or history"
            ],
            design_techniques: [
                "Flat design with strong outlines and clear separation of elements",
                "Subtle gradients or shadows for depth",
                "Emphasis on clean lines and simplified forms",
                "Effective use of negative space for visual impact"
            ],
            mood_and_atmosphere: [
                "Aggressive and powerful",
                "Loyal and traditional",
                "Energetic and competitive",
                "Representing strength and determination"
            ]
        };
        
        this.init();
    }

    async init() {
        try {
            await this.loadTeams();
            this.setupEventListeners();
            this.populateFilters();
            this.renderTeams();
        } catch (error) {
            console.error('Error initializing dashboard:', error);
        }
    }

    async loadTeams() {
        try {
            const response = await fetch('api.php?action=getTeams');
            if (!response.ok) {
                // Fallback to local JSON file
                const fallbackResponse = await fetch('nfl_logos.json');
                const data = await fallbackResponse.json();
                this.teams = data.teams;
            } else {
                const data = await response.json();
                this.teams = data.teams || data;
            }
            this.filteredTeams = [...this.teams];
        } catch (error) {
            console.error('Error loading teams:', error);
            // Fallback data if everything fails
            this.teams = this.getFallbackTeams();
            this.filteredTeams = [...this.teams];
        }
    }

    getFallbackTeams() {
        return [
            {
                id: 1,
                name: "Kansas City Chiefs",
                city: "Kansas City",
                mascot: "Chiefs",
                conference: "AFC",
                division: "West",
                colors: { primary: "#E31837", secondary: "#FFB81C", accent: "#FFFFFF" },
                founded: 1960
            },
            {
                id: 2,
                name: "Tampa Bay Buccaneers",
                city: "Tampa Bay", 
                mascot: "Buccaneers",
                conference: "NFC",
                division: "South",
                colors: { primary: "#D50A0A", secondary: "#FF7900", accent: "#0A0A08" },
                founded: 1974
            }
        ];
    }

    setupEventListeners() {
        // Team selection
        const teamSelect = document.getElementById('teamSelect');
        teamSelect.addEventListener('change', (e) => {
            const teamId = parseInt(e.target.value);
            this.selectedTeam = this.teams.find(team => team.id === teamId);
            if (this.selectedTeam) {
                this.openLogoModal(this.selectedTeam);
            }
        });

        // Filters
        document.getElementById('conferenceFilter').addEventListener('change', () => this.applyFilters());
        document.getElementById('divisionFilter').addEventListener('change', () => this.applyFilters());

        // Generate button
        document.getElementById('generateBtn').addEventListener('click', () => {
            if (this.selectedTeam) {
                this.generateLogoVariations(this.selectedTeam);
            } else {
                alert('Please select a team first!');
            }
        });

        // Modal controls
        document.getElementById('closeModal').addEventListener('click', () => this.closeModal());
        document.getElementById('logoModal').addEventListener('click', (e) => {
            if (e.target.id === 'logoModal') {
                this.closeModal();
            }
        });

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.closeModal();
            }
        });
    }

    populateFilters() {
        const teamSelect = document.getElementById('teamSelect');
        
        // Clear existing options
        teamSelect.innerHTML = '<option value="">Choose a team...</option>';
        
        // Populate team select
        this.teams.forEach(team => {
            const option = document.createElement('option');
            option.value = team.id;
            option.textContent = team.name;
            teamSelect.appendChild(option);
        });
    }

    applyFilters() {
        const conferenceFilter = document.getElementById('conferenceFilter').value;
        const divisionFilter = document.getElementById('divisionFilter').value;

        this.filteredTeams = this.teams.filter(team => {
            const matchesConference = !conferenceFilter || team.conference === conferenceFilter;
            const matchesDivision = !divisionFilter || team.division === divisionFilter;
            return matchesConference && matchesDivision;
        });

        this.renderTeams();
    }

    renderTeams() {
        const teamGrid = document.getElementById('teamGrid');
        teamGrid.innerHTML = '';

        this.filteredTeams.forEach(team => {
            const teamCard = this.createTeamCard(team);
            teamGrid.appendChild(teamCard);
        });
    }

    createTeamCard(team) {
        const card = document.createElement('div');
        card.className = 'team-card fade-in';
        card.style.animationDelay = `${Math.random() * 0.5}s`;

        const logoUrl = team.logo || `https://via.placeholder.com/80x80/${team.colors.primary.slice(1)}/ffffff?text=${team.mascot.charAt(0)}`;

        card.innerHTML = `
            <img src="${logoUrl}" alt="${team.name} Logo" class="team-logo" 
                 onerror="this.src='https://via.placeholder.com/80x80/${team.colors.primary.slice(1)}/ffffff?text=${team.mascot.charAt(0)}'">
            <h3 class="team-name">${team.name}</h3>
            <div class="team-details">
                ${team.conference} ${team.division} • Founded ${team.founded}
            </div>
            <div class="team-colors">
                <div class="color-swatch" style="background-color: ${team.colors.primary}"></div>
                <div class="color-swatch" style="background-color: ${team.colors.secondary}"></div>
                <div class="color-swatch" style="background-color: ${team.colors.accent}"></div>
            </div>
            <button class="view-variations-btn" onclick="dashboard.openLogoModal(${JSON.stringify(team).replace(/"/g, '&quot;')})">
                <i class="fas fa-eye"></i> View Logo Variations
            </button>
        `;

        return card;
    }

    openLogoModal(team) {
        this.selectedTeam = team;
        
        // Update modal content
        document.getElementById('modalTeamName').textContent = `${team.name} - Logo Variations`;
        document.getElementById('teamDetails').textContent = 
            `${team.conference} ${team.division} • Founded ${team.founded} • ${team.city}`;

        // Set current logo
        const currentLogo = document.getElementById('currentLogo');
        const logoUrl = team.logo || `https://via.placeholder.com/200x200/${team.colors.primary.slice(1)}/ffffff?text=${team.mascot}`;
        currentLogo.src = logoUrl;
        currentLogo.alt = `${team.name} Current Logo`;

        // Generate logo variations
        this.generateLogoVariations(team);

        // Show modal
        document.getElementById('logoModal').style.display = 'block';
        document.body.style.overflow = 'hidden';
    }

    closeModal() {
        document.getElementById('logoModal').style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    generateLogoVariations(team) {
        this.showLoading();
        
        // Simulate generation delay for better UX
        setTimeout(() => {
            this.createMinimalistVariation(team);
            this.createRetroVariation(team);
            this.hideLoading();
        }, 1500);
    }

    createMinimalistVariation(team) {
        const canvas = document.getElementById('logoCanvas1');
        const ctx = canvas.getContext('2d');
        
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Set canvas size
        canvas.width = 200;
        canvas.height = 200;

        // Modern Minimalist Design
        this.drawMinimalistLogo(ctx, team, canvas.width, canvas.height);
    }

    createRetroVariation(team) {
        const canvas = document.getElementById('logoCanvas2');
        const ctx = canvas.getContext('2d');
        
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Set canvas size
        canvas.width = 200;
        canvas.height = 200;

        // Retro Classic Design
        this.drawRetroLogo(ctx, team, canvas.width, canvas.height);
    }

    drawMinimalistLogo(ctx, team, width, height) {
        const centerX = width / 2;
        const centerY = height / 2;
        const radius = Math.min(width, height) * 0.35;

        // Background circle with team primary color
        ctx.fillStyle = team.colors.primary;
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
        ctx.fill();

        // Inner circle with secondary color
        ctx.fillStyle = team.colors.secondary;
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius * 0.7, 0, 2 * Math.PI);
        ctx.fill();

        // Team initial in the center
        ctx.fillStyle = team.colors.accent;
        ctx.font = `bold ${radius * 0.8}px Arial`;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(team.mascot.charAt(0), centerX, centerY);

        // Clean border
        ctx.strokeStyle = '#ffffff';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius, 0, 2 * Math.PI);
        ctx.stroke();
    }

    drawRetroLogo(ctx, team, width, height) {
        const centerX = width / 2;
        const centerY = height / 2;

        // Create shield shape
        this.drawShield(ctx, centerX, centerY, width * 0.35, height * 0.4, team);

        // Add vintage text
        ctx.fillStyle = team.colors.primary;
        ctx.font = 'bold 16px serif';
        ctx.textAlign = 'center';
        ctx.fillText(team.city.toUpperCase(), centerX, centerY - height * 0.15);
        
        ctx.font = 'bold 14px serif';
        ctx.fillText(team.mascot.toUpperCase(), centerX, centerY + height * 0.25);

        // Add decorative elements
        this.addRetroDecorations(ctx, centerX, centerY, width, height, team);
    }

    drawShield(ctx, centerX, centerY, width, height, team) {
        ctx.fillStyle = team.colors.primary;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY - height);
        ctx.lineTo(centerX - width, centerY - height * 0.3);
        ctx.lineTo(centerX - width, centerY + height * 0.3);
        ctx.lineTo(centerX, centerY + height);
        ctx.lineTo(centerX + width, centerY + height * 0.3);
        ctx.lineTo(centerX + width, centerY - height * 0.3);
        ctx.closePath();
        ctx.fill();

        // Inner shield
        ctx.fillStyle = team.colors.secondary;
        ctx.beginPath();
        ctx.moveTo(centerX, centerY - height * 0.7);
        ctx.lineTo(centerX - width * 0.7, centerY - height * 0.1);
        ctx.lineTo(centerX - width * 0.7, centerY + height * 0.1);
        ctx.lineTo(centerX, centerY + height * 0.7);
        ctx.lineTo(centerX + width * 0.7, centerY + height * 0.1);
        ctx.lineTo(centerX + width * 0.7, centerY - height * 0.1);
        ctx.closePath();
        ctx.fill();

        // Team initial
        ctx.fillStyle = team.colors.accent;
        ctx.font = 'bold 32px serif';
        ctx.textAlign = 'center';
        ctx.textBaseline = 'middle';
        ctx.fillText(team.mascot.charAt(0), centerX, centerY);
    }

    addRetroDecorations(ctx, centerX, centerY, width, height, team) {
        // Add stars
        ctx.fillStyle = team.colors.secondary;
        this.drawStar(ctx, centerX - width * 0.3, centerY - height * 0.3, 8, 5, 3);
        this.drawStar(ctx, centerX + width * 0.3, centerY - height * 0.3, 8, 5, 3);

        // Add founding year
        ctx.fillStyle = team.colors.primary;
        ctx.font = 'bold 10px serif';
        ctx.textAlign = 'center';
        ctx.fillText(`EST. ${team.founded}`, centerX, centerY + height * 0.35);
    }

    drawStar(ctx, cx, cy, spikes, outerRadius, innerRadius) {
        let rot = Math.PI / 2 * 3;
        let x = cx;
        let y = cy;
        const step = Math.PI / spikes;

        ctx.beginPath();
        ctx.moveTo(cx, cy - outerRadius);
        
        for (let i = 0; i < spikes; i++) {
            x = cx + Math.cos(rot) * outerRadius;
            y = cy + Math.sin(rot) * outerRadius;
            ctx.lineTo(x, y);
            rot += step;

            x = cx + Math.cos(rot) * innerRadius;
            y = cy + Math.sin(rot) * innerRadius;
            ctx.lineTo(x, y);
            rot += step;
        }
        
        ctx.lineTo(cx, cy - outerRadius);
        ctx.closePath();
        ctx.fill();
    }

    showLoading() {
        document.getElementById('loadingOverlay').style.display = 'flex';
    }

    hideLoading() {
        document.getElementById('loadingOverlay').style.display = 'none';
    }
}

// Logo download functionality
function downloadLogo(canvasId) {
    const canvas = document.getElementById(canvasId);
    const link = document.createElement('a');
    link.download = `${dashboard.selectedTeam.name.replace(/\s+/g, '_')}_logo_variation.png`;
    link.href = canvas.toDataURL();
    link.click();
}

// Initialize dashboard
let dashboard;
document.addEventListener('DOMContentLoaded', () => {
    dashboard = new NFLLogoDashboard();
});

// Utility functions
function hexToRgb(hex) {
    const result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? {
        r: parseInt(result[1], 16),
        g: parseInt(result[2], 16),
        b: parseInt(result[3], 16)
    } : null;
}

function rgbToHex(r, g, b) {
    return "#" + ((1 << 24) + (r << 16) + (g << 8) + b).toString(16).slice(1);
}

// Add smooth scrolling for better UX
function smoothScroll(target) {
    document.querySelector(target).scrollIntoView({
        behavior: 'smooth'
    });
}

// Add intersection observer for animations
const observeElements = () => {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('slide-up');
            }
        });
    });

    document.querySelectorAll('.team-card').forEach(card => {
        observer.observe(card);
    });
};

// Call observer when teams are rendered
document.addEventListener('teamsRendered', observeElements);