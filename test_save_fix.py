#!/usr/bin/env python3
"""
Test that auto-save has been removed and only explicit saves remain
"""

import sys
sys.path.append('.')

def test_auto_save_removal():
    print("=== Testing Auto-Save Removal ===")
    
    # Read the main_game.py file and check for problematic auto-saves
    with open('/home/rydloj/Projects/Mini-Portal-Game/pygame_version/game/main_game.py', 'r') as f:
        content = f.read()
    
    # Check for removed auto-saves
    issues = []
    
    # 1. Check quit method doesn't auto-save
    if 'def quit(self):' in content:
        quit_section = content[content.find('def quit(self):'):content.find('def quit(self):') + 200]
        if 'self.save_game()' in quit_section:
            issues.append("❌ quit() method still contains auto-save")
        else:
            print("✅ quit() method no longer auto-saves")
    
    # 2. Check for periodic auto-save removal
    if 'auto_save_timer' in content and 'self.save_game()' in content:
        issues.append("❌ Periodic auto-save still exists")
    else:
        print("✅ Periodic auto-save removed")
    
    # 3. Check level completion auto-save removal
    level_completion_lines = [line for line in content.split('\n') if 'game_state == "won"' in line]
    for line in level_completion_lines:
        if 'self.save_game()' in line:
            issues.append("❌ Level completion auto-save still exists")
            break
    else:
        print("✅ Level completion auto-save removed")
    
    # 4. Check exit to main auto-save removal
    exit_main_lines = [line for line in content.split('\n') if 'exit_to_main' in line]
    found_save_in_exit = False
    for i, line in enumerate(content.split('\n')):
        if 'exit_to_main' in line:
            # Check next few lines for save_game call
            next_lines = content.split('\n')[i:i+5]
            if any('self.save_game()' in l for l in next_lines):
                found_save_in_exit = True
                break
    
    if found_save_in_exit:
        issues.append("❌ Exit to main auto-save still exists")
    else:
        print("✅ Exit to main auto-save removed")
    
    # 5. Check that explicit saves remain
    explicit_save_count = content.count('save_slot_')
    if explicit_save_count > 0:
        print(f"✅ Explicit save functionality preserved ({explicit_save_count} references)")
    else:
        issues.append("❌ Explicit save functionality might be broken")
    
    if not issues:
        print("\n🎉 AUTO-SAVE REMOVAL SUCCESSFUL!")
        print("\nNow saves only happen when:")
        print("  - User explicitly selects a save slot from pause menu")
        print("  - User uses manual save options")
        print("\nNo more unwanted overwrites of slot 0!")
        return True
    else:
        print("\n❌ Issues found:")
        for issue in issues:
            print(f"  {issue}")
        return False

if __name__ == "__main__":
    success = test_auto_save_removal()
    exit(0 if success else 1)