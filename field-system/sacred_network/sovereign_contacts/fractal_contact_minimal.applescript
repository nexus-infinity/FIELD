-- Fractal Contact Intelligence - Minimal Safe Version
-- This version is designed to avoid freezing with large contact databases

property batchSize : 5 -- Very small batch size for safety
property timeoutSeconds : 10 -- Short timeout to avoid freezing

-- Simple startup
display dialog "🧬 Fractal Contact Intelligence - Safe Mode" & return & return & "This minimal version processes contacts safely without freezing." buttons {"Cancel", "Start"} default button 2

if button returned of result is "Cancel" then
	return
end if

-- Test contacts access first
set contactCount to 0
try
	with timeout of 5 seconds
		tell application "Contacts"
			set contactCount to count of every person
		end tell
	end timeout
on error errMsg
	display dialog "❌ Cannot access Contacts:" & return & errMsg buttons {"OK"}
	return
end try

-- Show count and ask to proceed
if contactCount = 0 then
	display dialog "📭 No contacts found in database" buttons {"OK"}
	return
else if contactCount > 100 then
	display dialog "⚠️ Large database detected: " & contactCount & " contacts" & return & return & "Processing only first 50 contacts for safety." buttons {"Cancel", "Continue"} default button 2
	if button returned of result is "Cancel" then
		return
	end if
	set contactCount to 50 -- Limit for safety
end if

-- Process contacts in tiny batches
set processedCount to 0
set duplicates to {}

display dialog "Processing " & contactCount & " contacts..." giving up after 2

try
	tell application "Contacts"
		-- Get just the first batch of contacts
		if contactCount > 10 then
			set testContacts to items 1 through 10 of every person
		else
			set testContacts to every person
		end if
		
		-- Simple duplicate check on names only
		repeat with i from 1 to count of testContacts
			set contact1 to item i of testContacts
			try
				set name1 to name of contact1
			on error
				set name1 to "Unknown"
			end try
			
			repeat with j from (i + 1) to count of testContacts
				set contact2 to item j of testContacts
				try
					set name2 to name of contact2
				on error
					set name2 to "Unknown"
				end try
				
				if name1 = name2 and name1 is not "Unknown" then
					set duplicates to duplicates & {name1}
				end if
			end repeat
		end repeat
	end tell
	
	-- Show results
	set duplicateCount to count of duplicates
	display dialog "✅ Analysis Complete!" & return & return & "Contacts checked: " & (count of testContacts) & return & "Duplicates found: " & duplicateCount buttons {"OK"}
	
on error errMsg
	display dialog "❌ Error during processing:" & return & errMsg buttons {"OK"}
end try
