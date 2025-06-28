// ==UserScript==
// @name         TikTok Live Users Extractor
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Extract 20 random live user names from TikTok live page
// @author       You
// @match        https://tiktok.com/live*
// @match        https://www.tiktok.com/live*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Function to extract usernames from live streams
    function extractLiveUsernames() {
        const usernames = new Set();
        
        // Common selectors for TikTok live user elements
        const selectors = [
            '[data-e2e="live-avatar"] + div',
            '[data-e2e="live-card-username"]',
            'a[href*="/@"] span',
            'div[data-e2e*="user"] span',
            '.live-card-username',
            '.live-stream-username',
            'span[data-e2e*="username"]'
        ];
        
        // Try multiple selectors to find usernames
        selectors.forEach(selector => {
            const elements = document.querySelectorAll(selector);
            elements.forEach(element => {
                let text = element.textContent?.trim();
                if (text) {
                    // Remove @ symbol if present
                    text = text.replace(/^@/, '');
                    // Only add if it looks like a username (no spaces, reasonable length, not LIVE)
                    if (text.length > 0 && text.length < 50 && !text.includes(' ') && !text.includes('\n') && text.toUpperCase() !== 'LIVE') {
                        usernames.add(text);
                    }
                }
            });
        });
        
        // Also check href attributes for usernames
        const links = document.querySelectorAll('a[href*="/@"]');
        links.forEach(link => {
            const href = link.getAttribute('href');
            const match = href.match(/@([^/?&]+)/);
            if (match && match[1]) {
                usernames.add(match[1]);
            }
        });
        
        return Array.from(usernames);
    }
    
    // Function to shuffle array and get random subset
    function getRandomUsers(users, count = 20) {
        const shuffled = users.sort(() => 0.5 - Math.random());
        return shuffled.slice(0, Math.min(count, shuffled.length));
    }
    
    // Function to copy text to clipboard
    async function copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (err) {
            // Fallback method
            const textArea = document.createElement('textarea');
            textArea.value = text;
            document.body.appendChild(textArea);
            textArea.select();
            document.execCommand('copy');
            document.body.removeChild(textArea);
            return true;
        }
    }
    
    // Function to show notification
    function showNotification(message, isError = false) {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: ${isError ? '#ff4444' : '#4CAF50'};
            color: white;
            padding: 12px 20px;
            border-radius: 4px;
            z-index: 10000;
            font-family: Arial, sans-serif;
            font-size: 14px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
        `;
        notification.textContent = message;
        document.body.appendChild(notification);
        
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 3000);
    }
    
    // Main extraction function
    function extractAndCopyUsernames() {
        const allUsers = extractLiveUsernames();
        
        if (allUsers.length === 0) {
            showNotification('No live users found. Make sure the page is fully loaded.', true);
            return;
        }
        
        const randomUsers = getRandomUsers(allUsers, 20);
        const result = randomUsers.join(' ');
        
        copyToClipboard(result).then(() => {
            showNotification(`Copied ${randomUsers.length} usernames to clipboard!`);
            console.log('Extracted usernames:', result);
        }).catch(() => {
            showNotification('Failed to copy to clipboard', true);
        });
    }
    
    // Create and add extraction button
    function createExtractionButton() {
        const button = document.createElement('button');
        button.textContent = 'Extract Live Users';
        button.style.cssText = `
            position: fixed;
            top: 20px;
            left: 20px;
            background: #ff0050;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 6px;
            cursor: pointer;
            z-index: 10000;
            font-family: Arial, sans-serif;
            font-size: 14px;
            font-weight: bold;
            box-shadow: 0 2px 10px rgba(0,0,0,0.3);
            transition: background 0.2s;
        `;
        
        button.addEventListener('mouseenter', () => {
            button.style.background = '#e6004a';
        });
        
        button.addEventListener('mouseleave', () => {
            button.style.background = '#ff0050';
        });
        
        button.addEventListener('click', extractAndCopyUsernames);
        
        document.body.appendChild(button);
    }
    
    // Wait for page to load and create button
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(createExtractionButton, 2000);
        });
    } else {
        setTimeout(createExtractionButton, 2000);
    }
    
    // Also add keyboard shortcut (Ctrl+Shift+E)
    document.addEventListener('keydown', (e) => {
        if (e.ctrlKey && e.shiftKey && e.key === 'E') {
            e.preventDefault();
            extractAndCopyUsernames();
        }
    });
    
})();
