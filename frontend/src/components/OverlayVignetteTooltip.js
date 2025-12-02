/**
 * OverlayVignetteTooltip Component
 * 
 * A conditional UI component for displaying overlay vignette tooltips
 * with support for qualified_request inline or section states.
 * 
 * @module OverlayVignetteTooltip
 */

/**
 * Tooltip state enumeration
 * @typedef {'idle' | 'hovering' | 'active' | 'qualified' | 'pending' | 'error'} TooltipState
 */

/**
 * Qualified request status
 * @typedef {'none' | 'inline' | 'section'} QualifiedRequestMode
 */

/**
 * Tooltip configuration object
 * @typedef {Object} TooltipConfig
 * @property {string} content - Tooltip content text
 * @property {string} [title] - Optional tooltip title
 * @property {TooltipState} state - Current UI state
 * @property {QualifiedRequestMode} qualifiedMode - Qualified request display mode
 * @property {boolean} showVignette - Whether to show vignette overlay
 * @property {number} [duration] - Auto-hide duration in ms
 * @property {Object} [position] - Position configuration
 */

const OverlayVignetteTooltip = {
    // ============ State Management ============
    
    /** @type {Map<string, TooltipConfig>} */
    tooltips: new Map(),
    
    /** @type {HTMLElement|null} */
    activeTooltip: null,
    
    /** @type {HTMLElement|null} */
    vignetteOverlay: null,
    
    // ============ Constants ============
    
    STATES: {
        IDLE: 'idle',
        HOVERING: 'hovering',
        ACTIVE: 'active',
        QUALIFIED: 'qualified',
        PENDING: 'pending',
        ERROR: 'error'
    },
    
    QUALIFIED_MODES: {
        NONE: 'none',
        INLINE: 'inline',
        SECTION: 'section'
    },
    
    // Default configuration
    defaults: {
        state: 'idle',
        qualifiedMode: 'none',
        showVignette: false,
        duration: 0,
        position: {
            anchor: 'bottom',
            offset: { x: 0, y: 8 }
        }
    },
    
    // ============ Initialization ============
    
    /**
     * Initializes the tooltip system
     */
    init() {
        this._injectStyles();
        this._createVignetteOverlay();
        this._bindGlobalEvents();
        console.log('OverlayVignetteTooltip initialized');
    },
    
    /**
     * Injects required CSS styles
     * @private
     */
    _injectStyles() {
        if (document.getElementById('overlay-vignette-tooltip-styles')) return;
        
        const style = document.createElement('style');
        style.id = 'overlay-vignette-tooltip-styles';
        style.textContent = `
            /* Vignette Overlay */
            .vignette-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: radial-gradient(ellipse at center, transparent 0%, rgba(0,0,0,0.7) 100%);
                opacity: 0;
                pointer-events: none;
                transition: opacity 0.3s ease-in-out;
                z-index: 9998;
            }
            
            .vignette-overlay.active {
                opacity: 1;
                pointer-events: auto;
            }
            
            /* Tooltip Container */
            .ovt-tooltip {
                position: absolute;
                max-width: 320px;
                padding: 12px 16px;
                border-radius: 8px;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                font-size: 14px;
                line-height: 1.5;
                box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
                z-index: 9999;
                opacity: 0;
                transform: translateY(10px);
                transition: opacity 0.2s ease, transform 0.2s ease;
            }
            
            .ovt-tooltip.visible {
                opacity: 1;
                transform: translateY(0);
            }
            
            /* State Variations */
            .ovt-tooltip.state-idle {
                background: #ffffff;
                color: #333333;
                border: 1px solid #e0e0e0;
            }
            
            .ovt-tooltip.state-hovering {
                background: #f8f9fa;
                color: #333333;
                border: 1px solid #dee2e6;
            }
            
            .ovt-tooltip.state-active {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: #ffffff;
                border: none;
            }
            
            .ovt-tooltip.state-qualified {
                background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
                color: #ffffff;
                border: none;
            }
            
            .ovt-tooltip.state-pending {
                background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
                color: #ffffff;
                border: none;
            }
            
            .ovt-tooltip.state-error {
                background: #dc3545;
                color: #ffffff;
                border: none;
            }
            
            /* Tooltip Title */
            .ovt-tooltip-title {
                font-weight: 600;
                margin-bottom: 8px;
                font-size: 15px;
            }
            
            /* Tooltip Content */
            .ovt-tooltip-content {
                margin: 0;
            }
            
            /* Qualified Request Inline */
            .ovt-qualified-inline {
                display: inline-flex;
                align-items: center;
                gap: 6px;
                margin-top: 10px;
                padding: 6px 10px;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 4px;
                font-size: 12px;
                font-weight: 500;
            }
            
            .ovt-qualified-inline .status-icon {
                width: 16px;
                height: 16px;
            }
            
            /* Qualified Request Section */
            .ovt-qualified-section {
                margin-top: 12px;
                padding-top: 12px;
                border-top: 1px solid rgba(255, 255, 255, 0.2);
            }
            
            .ovt-qualified-section-title {
                font-size: 11px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                opacity: 0.8;
                margin-bottom: 6px;
            }
            
            .ovt-qualified-section-content {
                display: flex;
                flex-direction: column;
                gap: 4px;
            }
            
            .ovt-qualified-item {
                display: flex;
                align-items: center;
                gap: 8px;
                font-size: 13px;
            }
            
            .ovt-qualified-item .check-icon {
                color: #38ef7d;
            }
            
            /* Arrow */
            .ovt-tooltip-arrow {
                position: absolute;
                width: 0;
                height: 0;
                border-style: solid;
            }
            
            .ovt-tooltip-arrow.bottom {
                top: -8px;
                left: 50%;
                transform: translateX(-50%);
                border-width: 0 8px 8px 8px;
                border-color: transparent transparent currentColor transparent;
            }
            
            .ovt-tooltip-arrow.top {
                bottom: -8px;
                left: 50%;
                transform: translateX(-50%);
                border-width: 8px 8px 0 8px;
                border-color: currentColor transparent transparent transparent;
            }
            
            /* Animation for qualified state */
            @keyframes qualifiedPulse {
                0%, 100% { box-shadow: 0 4px 20px rgba(56, 239, 125, 0.3); }
                50% { box-shadow: 0 4px 30px rgba(56, 239, 125, 0.5); }
            }
            
            .ovt-tooltip.state-qualified {
                animation: qualifiedPulse 2s ease-in-out infinite;
            }
            
            /* Close button */
            .ovt-close-btn {
                position: absolute;
                top: 8px;
                right: 8px;
                width: 20px;
                height: 20px;
                border: none;
                background: rgba(255, 255, 255, 0.2);
                border-radius: 50%;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 12px;
                color: inherit;
                opacity: 0.7;
                transition: opacity 0.2s;
            }
            
            .ovt-close-btn:hover {
                opacity: 1;
            }
        `;
        
        document.head.appendChild(style);
    },
    
    /**
     * Creates the vignette overlay element
     * @private
     */
    _createVignetteOverlay() {
        if (document.getElementById('vignette-overlay')) return;
        
        this.vignetteOverlay = document.createElement('div');
        this.vignetteOverlay.id = 'vignette-overlay';
        this.vignetteOverlay.className = 'vignette-overlay';
        this.vignetteOverlay.addEventListener('click', () => this.hideAll());
        document.body.appendChild(this.vignetteOverlay);
    },
    
    /**
     * Binds global event listeners
     * @private
     */
    _bindGlobalEvents() {
        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') {
                this.hideAll();
            }
        });
    },
    
    // ============ Core Methods ============
    
    /**
     * Creates and registers a new tooltip
     * @param {string} id - Unique identifier for the tooltip
     * @param {Partial<TooltipConfig>} config - Tooltip configuration
     * @returns {HTMLElement} The tooltip element
     */
    create(id, config) {
        const mergedConfig = { ...this.defaults, ...config };
        this.tooltips.set(id, mergedConfig);
        
        const element = this._createTooltipElement(id, mergedConfig);
        document.body.appendChild(element);
        
        return element;
    },
    
    /**
     * Shows a tooltip
     * @param {string} id - Tooltip identifier
     * @param {HTMLElement} [anchor] - Element to anchor the tooltip to
     */
    show(id, anchor = null) {
        const config = this.tooltips.get(id);
        if (!config) {
            console.warn(`Tooltip "${id}" not found`);
            return;
        }
        
        let element = document.getElementById(`ovt-${id}`);
        if (!element) {
            element = this._createTooltipElement(id, config);
            document.body.appendChild(element);
        }
        
        // Update content based on current config
        this._updateTooltipContent(element, config);
        
        // Position tooltip
        if (anchor) {
            this._positionTooltip(element, anchor, config.position);
        }
        
        // Show vignette if configured
        if (config.showVignette && this.vignetteOverlay) {
            this.vignetteOverlay.classList.add('active');
        }
        
        // Show tooltip
        requestAnimationFrame(() => {
            element.classList.add('visible');
        });
        
        this.activeTooltip = element;
        
        // Auto-hide if duration is set
        if (config.duration > 0) {
            setTimeout(() => this.hide(id), config.duration);
        }
    },
    
    /**
     * Hides a tooltip
     * @param {string} id - Tooltip identifier
     */
    hide(id) {
        const element = document.getElementById(`ovt-${id}`);
        if (element) {
            element.classList.remove('visible');
        }
        
        // Hide vignette
        if (this.vignetteOverlay) {
            this.vignetteOverlay.classList.remove('active');
        }
        
        this.activeTooltip = null;
    },
    
    /**
     * Hides all visible tooltips
     */
    hideAll() {
        this.tooltips.forEach((_, id) => {
            this.hide(id);
        });
    },
    
    /**
     * Updates tooltip state
     * @param {string} id - Tooltip identifier
     * @param {TooltipState} state - New state
     */
    setState(id, state) {
        const config = this.tooltips.get(id);
        if (config) {
            config.state = state;
            this.tooltips.set(id, config);
            
            const element = document.getElementById(`ovt-${id}`);
            if (element) {
                // Remove existing state classes
                Object.values(this.STATES).forEach(s => {
                    element.classList.remove(`state-${s}`);
                });
                // Add new state class
                element.classList.add(`state-${state}`);
            }
        }
    },
    
    /**
     * Sets qualified request mode
     * @param {string} id - Tooltip identifier
     * @param {QualifiedRequestMode} mode - Qualified request display mode
     * @param {Object} [data] - Qualified request data
     */
    setQualifiedMode(id, mode, data = {}) {
        const config = this.tooltips.get(id);
        if (config) {
            config.qualifiedMode = mode;
            config.qualifiedData = data;
            this.tooltips.set(id, config);
            
            const element = document.getElementById(`ovt-${id}`);
            if (element) {
                this._updateTooltipContent(element, config);
            }
        }
    },
    
    /**
     * Updates tooltip configuration
     * @param {string} id - Tooltip identifier
     * @param {Partial<TooltipConfig>} updates - Configuration updates
     */
    update(id, updates) {
        const config = this.tooltips.get(id);
        if (config) {
            const newConfig = { ...config, ...updates };
            this.tooltips.set(id, newConfig);
            
            const element = document.getElementById(`ovt-${id}`);
            if (element) {
                this._updateTooltipContent(element, newConfig);
            }
        }
    },
    
    /**
     * Destroys a tooltip
     * @param {string} id - Tooltip identifier
     */
    destroy(id) {
        const element = document.getElementById(`ovt-${id}`);
        if (element) {
            element.remove();
        }
        this.tooltips.delete(id);
    },
    
    // ============ Private Helpers ============
    
    /**
     * Creates tooltip DOM element
     * @private
     * @param {string} id - Tooltip identifier
     * @param {TooltipConfig} config - Tooltip configuration
     * @returns {HTMLElement}
     */
    _createTooltipElement(id, config) {
        const element = document.createElement('div');
        element.id = `ovt-${id}`;
        element.className = `ovt-tooltip state-${config.state}`;
        element.setAttribute('role', 'tooltip');
        element.setAttribute('aria-hidden', 'true');
        
        this._updateTooltipContent(element, config);
        
        return element;
    },
    
    /**
     * Updates tooltip content
     * @private
     * @param {HTMLElement} element - Tooltip element
     * @param {TooltipConfig} config - Tooltip configuration
     */
    _updateTooltipContent(element, config) {
        let html = '';
        
        // Close button for active states
        if (config.state === this.STATES.ACTIVE || 
            config.state === this.STATES.QUALIFIED ||
            config.showVignette) {
            html += '<button class="ovt-close-btn" onclick="OverlayVignetteTooltip.hideAll()">×</button>';
        }
        
        // Title
        if (config.title) {
            html += `<div class="ovt-tooltip-title">${this._escapeHtml(config.title)}</div>`;
        }
        
        // Content
        html += `<p class="ovt-tooltip-content">${this._escapeHtml(config.content)}</p>`;
        
        // Qualified request - Inline mode
        if (config.qualifiedMode === this.QUALIFIED_MODES.INLINE) {
            html += `
                <div class="ovt-qualified-inline">
                    <svg class="status-icon" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                    </svg>
                    <span>${config.qualifiedData?.message || 'Request Qualified'}</span>
                </div>
            `;
        }
        
        // Qualified request - Section mode
        if (config.qualifiedMode === this.QUALIFIED_MODES.SECTION && config.qualifiedData) {
            html += `
                <div class="ovt-qualified-section">
                    <div class="ovt-qualified-section-title">Qualification Status</div>
                    <div class="ovt-qualified-section-content">
                        ${this._renderQualifiedItems(config.qualifiedData)}
                    </div>
                </div>
            `;
        }
        
        // Arrow
        const arrowPosition = config.position?.anchor === 'top' ? 'top' : 'bottom';
        html += `<div class="ovt-tooltip-arrow ${arrowPosition}"></div>`;
        
        element.innerHTML = html;
    },
    
    /**
     * Renders qualified items for section mode
     * @private
     * @param {Object} data - Qualified data
     * @returns {string} HTML string
     */
    _renderQualifiedItems(data) {
        const items = [];
        
        if (data.armScore !== undefined) {
            const armStatus = data.armScore >= 902 ? '✓' : '✗';
            items.push(`
                <div class="ovt-qualified-item">
                    <span class="check-icon">${armStatus}</span>
                    <span>ARM Score: ${(data.armScore / 1000).toFixed(3)}</span>
                </div>
            `);
        }
        
        if (data.esScore !== undefined) {
            const esStatus = data.esScore >= 50 ? '✓' : '✗';
            items.push(`
                <div class="ovt-qualified-item">
                    <span class="check-icon">${esStatus}</span>
                    <span>ES Score: ${data.esScore}</span>
                </div>
            `);
        }
        
        if (data.attestationCount !== undefined) {
            const attStatus = data.attestationCount >= 3 ? '✓' : '○';
            items.push(`
                <div class="ovt-qualified-item">
                    <span class="check-icon">${attStatus}</span>
                    <span>Attestations: ${data.attestationCount}/3</span>
                </div>
            `);
        }
        
        if (data.customItems) {
            data.customItems.forEach(item => {
                const icon = item.passed ? '✓' : '✗';
                items.push(`
                    <div class="ovt-qualified-item">
                        <span class="check-icon">${icon}</span>
                        <span>${this._escapeHtml(item.label)}</span>
                    </div>
                `);
            });
        }
        
        return items.join('');
    },
    
    /**
     * Positions tooltip relative to anchor element
     * @private
     * @param {HTMLElement} tooltip - Tooltip element
     * @param {HTMLElement} anchor - Anchor element
     * @param {Object} position - Position configuration
     */
    _positionTooltip(tooltip, anchor, position) {
        const anchorRect = anchor.getBoundingClientRect();
        const tooltipRect = tooltip.getBoundingClientRect();
        const offset = position?.offset || { x: 0, y: 8 };
        
        let top, left;
        
        switch (position?.anchor || 'bottom') {
            case 'top':
                top = anchorRect.top - tooltipRect.height - offset.y;
                left = anchorRect.left + (anchorRect.width - tooltipRect.width) / 2 + offset.x;
                break;
            case 'bottom':
            default:
                top = anchorRect.bottom + offset.y;
                left = anchorRect.left + (anchorRect.width - tooltipRect.width) / 2 + offset.x;
                break;
        }
        
        // Keep tooltip within viewport
        const viewportWidth = window.innerWidth;
        const viewportHeight = window.innerHeight;
        
        if (left < 10) left = 10;
        if (left + tooltipRect.width > viewportWidth - 10) {
            left = viewportWidth - tooltipRect.width - 10;
        }
        if (top < 10) top = 10;
        if (top + tooltipRect.height > viewportHeight - 10) {
            top = viewportHeight - tooltipRect.height - 10;
        }
        
        tooltip.style.top = `${top}px`;
        tooltip.style.left = `${left}px`;
    },
    
    /**
     * Escapes HTML entities
     * @private
     * @param {string} text - Text to escape
     * @returns {string} Escaped text
     */
    _escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
};

// Auto-initialize when DOM is ready
if (typeof document !== 'undefined') {
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => OverlayVignetteTooltip.init());
    } else {
        OverlayVignetteTooltip.init();
    }
}

// Export for global use
if (typeof window !== 'undefined') {
    window.OverlayVignetteTooltip = OverlayVignetteTooltip;
}

// Export for module systems
if (typeof module !== 'undefined' && module.exports) {
    module.exports = OverlayVignetteTooltip;
}
