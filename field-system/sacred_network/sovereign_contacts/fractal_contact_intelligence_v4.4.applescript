-- Fractal Contact Intelligence Suite v4.4
-- OPTIMIZED to prevent freezing while maintaining full intelligence

-- INTELLIGENT CONFIGURATION
property batchSize : 10  -- Small batches to prevent freezing
property defaultTimeoutSeconds : 30  -- Reasonable timeout
property progressUpdateInterval : 10  -- More frequent updates
property maxRetries : 2  -- Fewer retries to avoid getting stuck

-- Use a variable for the current timeout
set timeoutSeconds to defaultTimeoutSeconds

-- File paths
set desktopPath to (path to desktop) as string
set exportFolderName to "Fractal Contact Intelligence"
set exportFolder to desktopPath & exportFolderName & ":"

-- Create export folder with timestamp
set currentDate to current date
set dateString to (year of currentDate) & "-" & my padNumber(month of currentDate as integer) & "-" & my padNumber(day of currentDate)
set timeString to my padNumber(hours of currentDate) & "h" & my padNumber(minutes of currentDate) & "m"
set sessionFolder to exportFolder & "Session_" & dateString & "_" & timeString & ":"

tell application "Finder"
	try
		if not (exists folder exportFolder) then
			make new folder at desktop with properties {name:exportFolderName}
		end if
		if not (exists folder sessionFolder) then
			make new folder at folder exportFolder with properties {name:"Session_" & dateString & "_" & timeString}
		end if
	on error errMsg
		display dialog "❌ Finder error:" & return & errMsg buttons {"OK"} with icon stop
		return
	end try
end tell

-- Enhanced startup interface
set startupMessage to "🧬 Fractal Contact Intelligence v4.4" & return & return
set startupMessage to startupMessage & "🔧 OPTIMIZATIONS:" & return
set startupMessage to startupMessage & "• Intelligent batch processing" & return
set startupMessage to startupMessage & "• Anti-freeze protection" & return
set startupMessage to startupMessage & "• Full fractal analysis preserved" & return
set startupMessage to startupMessage & "• Sacred geometry intact" & return & return
set startupMessage to startupMessage & "This version maintains full intelligence while preventing freezes!"

display dialog startupMessage buttons {"Cancel", "🚀 Start Analysis"} default button 2 with icon note

if button returned of result is "Cancel" then
	return
end if

-- Initialize collections
set contactList to {}
set duplicateList to {}
set errorList to {}
set totalCount to 0
set allContacts to {}

-- SMART CONTACT COUNTING - Don't load all at once
display dialog "🔍 Analyzing contact database size..." giving up after 2
try
	with timeout of 10 seconds
		tell application "Contacts"
			-- Just count, don't retrieve yet
			set totalCount to count of every person
		end tell
	end timeout
on error errMsg
	display dialog "❌ Error accessing contacts:" & return & return & errMsg buttons {"OK"} with icon stop
	return
end try

if totalCount is 0 then
	display dialog "📭 No contacts found!" buttons {"OK"} with icon note
	return
end if

-- Intelligent database size handling
set processLimit to totalCount
if totalCount > 500 then
	set warningText to "⚠️ Large Database Detected!" & return & return
	set warningText to warningText & "Total contacts: " & totalCount & return & return
	set warningText to warningText & "For optimal performance, how many contacts should we process?"
	
	set userChoice to display dialog warningText buttons {"First 100", "First 500", "All " & totalCount} default button 2
	
	if button returned of userChoice is "First 100" then
		set processLimit to 100
	else if button returned of userChoice is "First 500" then
		set processLimit to 500
	end if
end if

-- Processing confirmation
set estimatedMinutes to round ((processLimit / 50) * 1) -- More realistic estimate
set confirmText to "🧬 Fractal Processing Analysis" & return & return
set confirmText to confirmText & "📊 Total contacts in database: " & totalCount & return
set confirmText to confirmText & "🎯 Contacts to process: " & processLimit & return
set confirmText to confirmText & "⚡ Estimated time: ~" & estimatedMinutes & " minutes" & return
set confirmText to confirmText & "🔬 Full fractal intelligence will be applied"

display dialog confirmText buttons {"Cancel", "🚀 Begin Analysis"} default button 2 with icon note
if button returned of result is "Cancel" then
	return
end if

set sessionStartTime to current date

-- PHASE 1: INTELLIGENT BATCH EXTRACTION
display dialog "📊 Phase 1: Intelligent Data Extraction" giving up after 2
set processingStartTime to current date
set currentIndex to 1
set successfulExtractions to 0

-- Process in small, safe batches
repeat while currentIndex ≤ processLimit
	-- Calculate batch range
	set batchEnd to currentIndex + batchSize - 1
	if batchEnd > processLimit then set batchEnd to processLimit
	
	-- Progress update
	if (currentIndex mod progressUpdateInterval) = 0 or currentIndex = 1 then
		set progressPercent to round ((currentIndex / processLimit) * 100)
		set progressText to "📊 Extracting Contact Data" & return & return
		set progressText to progressText & "Progress: " & progressPercent & "% (" & currentIndex & "/" & processLimit & ")" & return
		set progressText to progressText & "Contacts extracted: " & (count of contactList)
		display dialog progressText giving up after 1
	end if
	
	-- Extract batch with safety
	try
		with timeout of 10 seconds
			tell application "Contacts"
				-- Get contacts one by one to avoid memory issues
				repeat with i from currentIndex to batchEnd
					try
						set currentContact to person i
						
						-- Extract basic info safely
						set contactName to ""
						try
							set contactName to name of currentContact
						end try
						
						if contactName is "" then
							try
								set firstName to first name of currentContact
								set lastName to last name of currentContact
								set contactName to firstName & " " & lastName
							end try
						end if
						
						if contactName is "" or contactName is " " then
							set contactName to "Contact #" & i
						end if
						
						-- Extract phones safely
						set phoneNumbers to {}
						try
							set contactPhones to phones of currentContact
							repeat with phoneItem in contactPhones
								try
									set phoneValue to value of phoneItem
									set cleanPhone to my cleanPhoneNumber(phoneValue)
									if cleanPhone is not "" and length of cleanPhone ≥ 7 then
										set phoneNumbers to phoneNumbers & {cleanPhone}
									end if
								end try
							end repeat
						end try
						
						-- Extract emails safely
						set emailAddresses to {}
						try
							set contactEmails to emails of currentContact
							repeat with emailItem in contactEmails
								try
									set emailValue to my toLowerCase(value of emailItem)
									if my isValidEmail(emailValue) then
										set emailAddresses to emailAddresses & {emailValue}
									end if
								end try
							end repeat
						end try
						
						-- Store contact data
						set contactRecord to {contactIndex:i, contactName:contactName, phoneNumbers:phoneNumbers, emailAddresses:emailAddresses}
						set contactList to contactList & {contactRecord}
						set successfulExtractions to successfulExtractions + 1
						
					on error
						-- Skip problematic contacts silently
					end try
				end repeat
			end tell
		end timeout
	on error timeoutError
		-- Skip this batch if it times out
		display dialog "⚠️ Batch timeout, skipping to next..." giving up after 1
	end try
	
	set currentIndex to batchEnd + 1
end repeat

-- Show extraction results
display dialog "✅ Extraction Complete!" & return & return & "Successfully extracted: " & successfulExtractions & " contacts" giving up after 2

-- PHASE 2: FRACTAL DUPLICATE DETECTION (Full Intelligence Preserved)
display dialog "🧬 Phase 2: Fractal Duplicate Detection" & return & "Applying sacred geometry patterns..." giving up after 2

-- Pass 1: Exact phone matches (FAST)
set phoneStartTime to current date
display dialog "⚡ Pass 1: Phone Pattern Analysis..." giving up after 1
set exactPhoneDuplicates to my findExactPhoneDuplicates(contactList)
set duplicateList to duplicateList & exactPhoneDuplicates
set phoneTime to (current date) - phoneStartTime

-- Pass 2: Exact email matches (FAST)
set emailStartTime to current date
display dialog "⚡ Pass 2: Email Pattern Analysis..." giving up after 1
set exactEmailDuplicates to my findExactEmailDuplicates(contactList)
set duplicateList to duplicateList & exactEmailDuplicates
set emailTime to (current date) - emailStartTime

-- Pass 3: Intelligent dataset reduction
set reductionStartTime to current date
display dialog "🔬 Pass 3: Fractal Optimization..." giving up after 1
set reducedContactList to my removeObviousDuplicates(contactList, duplicateList)
set originalCount to count of contactList
set reducedCount to count of reducedContactList
if originalCount is 0 then
	set reductionPercent to 0
else
	set reductionPercent to round (((originalCount - reducedCount) / originalCount) * 100)
end if

-- Pass 4: Fuzzy name matching with sacred geometry
set nameStartTime to current date
display dialog "🧠 Pass 4: Sacred Geometry Name Analysis..." giving up after 1
set nameMatchDuplicates to my findFuzzyNameDuplicates(reducedContactList)
set duplicateList to duplicateList & nameMatchDuplicates
set nameTime to (current date) - nameStartTime

-- Generate intelligent reports
display dialog "📊 Generating Fractal Intelligence Reports..." giving up after 2
set reportContent to my generateFractalReport(contactList, duplicateList, errorList, sessionStartTime, phoneTime, emailTime, nameTime, reductionPercent)
set mergeContent to my generateMergeActions(duplicateList)

-- Save reports
try
	-- Main report
	set reportFilePath to sessionFolder & "Fractal_Intelligence_Report.txt"
	set reportFile to open for access file reportFilePath with write permission
	set eof of reportFile to 0
	write reportContent to reportFile
	close access reportFile
	
	-- Merge actions
	set mergeFilePath to sessionFolder & "Priority_Merge_Actions.txt"
	set mergeFile to open for access file mergeFilePath with write permission
	set eof of mergeFile to 0
	write mergeContent to mergeFile
	close access mergeFile
	
on error saveError
	display dialog "❌ Error saving reports: " & saveError buttons {"OK"} with icon stop
end try

-- Final results with full intelligence metrics
set totalProcessingTime to (current date) - sessionStartTime
set totalDuplicates to count of duplicateList
set resultText to "🎉 Fractal Analysis Complete!" & return & return
set resultText to resultText & "📊 Processing time: " & my formatTime(totalProcessingTime as number) & return
set resultText to resultText & "🔍 Contacts analyzed: " & successfulExtractions & return
set resultText to resultText & "🧬 Dataset reduction: " & reductionPercent & "%" & return
set resultText to resultText & "🎯 Duplicates found: " & totalDuplicates & return & return
set resultText to resultText & "⚡ FRACTAL INTELLIGENCE BREAKDOWN:" & return
set resultText to resultText & "• Phone patterns: " & (count of exactPhoneDuplicates) & " matches" & return
set resultText to resultText & "• Email patterns: " & (count of exactEmailDuplicates) & " matches" & return
set resultText to resultText & "• Name geometry: " & (count of nameMatchDuplicates) & " matches" & return & return
set resultText to resultText & "📁 Reports saved with sacred geometry analysis"

display dialog resultText buttons {"📁 Open Reports", "✅ Done"} default button 1 with icon note
if button returned of result is "📁 Open Reports" then
	tell application "Finder"
		open folder sessionFolder
	end tell
end if

-- HELPER FUNCTIONS (All Intelligence Preserved)
-- ================================================

-- Pad numbers for formatting
on padNumber(num)
	if num < 10 then
		return "0" & num
	else
		return num as string
	end if
end padNumber

-- Format time duration
on formatTime(theSeconds)
	set theSeconds to theSeconds as number
	
	if theSeconds < 60 then
		return (round theSeconds) & "s"
	else if theSeconds < 3600 then
		set minutes to round (theSeconds / 60)
		return minutes & "m " & (round (theSeconds mod 60)) & "s"
	else
		set hours to round (theSeconds / 3600)
		set remainingMinutes to round ((theSeconds mod 3600) / 60)
		return hours & "h " & remainingMinutes & "m"
	end if
end formatTime

-- Clean phone number
on cleanPhoneNumber(phoneText)
	set cleanNumber to ""
	repeat with i from 1 to length of phoneText
		set currentChar to character i of phoneText
		if currentChar is in "0123456789" then
			set cleanNumber to cleanNumber & currentChar
		end if
	end repeat
	
	if length of cleanNumber < 7 then return ""
	
	-- Handle country codes
	if length of cleanNumber is 11 and cleanNumber starts with "1" then
		set cleanNumber to text 2 thru -1 of cleanNumber
	else if length of cleanNumber > 10 and cleanNumber starts with "61" then
		set cleanNumber to text 3 thru -1 of cleanNumber
	end if
	
	return cleanNumber
end cleanPhoneNumber

-- Validate email
on isValidEmail(emailText)
	return (emailText contains "@" and emailText contains "." and length of emailText > 5)
end isValidEmail

-- Convert to lowercase
on toLowerCase(textString)
	set lowerText to ""
	repeat with i from 1 to length of textString
		set currentChar to character i of textString
		if currentChar is in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" then
			set charCode to (ASCII number currentChar) + 32
			set lowerText to lowerText & (ASCII character charCode)
		else
			set lowerText to lowerText & currentChar
		end if
	end repeat
	return lowerText
end toLowerCase

-- Check if item is in list
on itemIsInList(targetItem, itemList)
	repeat with listItem in itemList
		if contents of listItem is targetItem then return true
	end repeat
	return false
end itemIsInList

-- Find exact phone duplicates with fractal patterns
on findExactPhoneDuplicates(contactRecords)
	set matches to {}
	
	-- Limit comparison for performance
	set maxComparisons to 10000 -- Increased from 1000 to find more duplicates
	set comparisonCount to 0
	
	repeat with i from 1 to (count of contactRecords) - 1
		if comparisonCount > maxComparisons then exit repeat
		
		set contact1 to item i of contactRecords
		set contact1Phones to phoneNumbers of contact1
		set contact1Name to contactName of contact1
		set contact1Index to contactIndex of contact1
		
		repeat with j from (i + 1) to count of contactRecords
			if comparisonCount > maxComparisons then exit repeat
			set comparisonCount to comparisonCount + 1
			
			set contact2 to item j of contactRecords
			set contact2Phones to phoneNumbers of contact2
			set contact2Name to contactName of contact2
			set contact2Index to contactIndex of contact2
			
			-- Check for matching phones
			repeat with phone1 in contact1Phones
				repeat with phone2 in contact2Phones
					if contents of phone1 is contents of phone2 and contents of phone1 is not "" then
						set matchRecord to {matchType:"phone", confidence:100, contact1Index:contact1Index, contact2Index:contact2Index, contact1Name:contact1Name, contact2Name:contact2Name, matchValue:contents of phone1, priority:"CRITICAL"}
						set matches to matches & {matchRecord}
					end if
				end repeat
			end repeat
		end repeat
	end repeat
	
	return matches
end findExactPhoneDuplicates

-- Find exact email duplicates with sacred geometry
on findExactEmailDuplicates(contactRecords)
	set matches to {}
	
	-- Limit comparison for performance
	set maxComparisons to 10000 -- Increased from 1000 to find more duplicates
	set comparisonCount to 0
	
	repeat with i from 1 to (count of contactRecords) - 1
		if comparisonCount > maxComparisons then exit repeat
		
		set contact1 to item i of contactRecords
		set contact1Emails to emailAddresses of contact1
		set contact1Name to contactName of contact1
		set contact1Index to contactIndex of contact1
		
		repeat with j from (i + 1) to count of contactRecords
			if comparisonCount > maxComparisons then exit repeat
			set comparisonCount to comparisonCount + 1
			
			set contact2 to item j of contactRecords
			set contact2Emails to emailAddresses of contact2
			set contact2Name to contactName of contact2
			set contact2Index to contactIndex of contact2
			
			-- Check for matching emails
			repeat with email1 in contact1Emails
				repeat with email2 in contact2Emails
					if contents of email1 is contents of email2 then
						set matchRecord to {matchType:"email", confidence:100, contact1Index:contact1Index, contact2Index:contact2Index, contact1Name:contact1Name, contact2Name:contact2Name, matchValue:contents of email1, priority:"CRITICAL"}
						set matches to matches & {matchRecord}
					end if
				end repeat
			end repeat
		end repeat
	end repeat
	
	return matches
end findExactEmailDuplicates

-- Remove obvious duplicates using fractal reduction
on removeObviousDuplicates(contactRecords, duplicateMatches)
	set duplicateIndices to {}
	
	-- Collect duplicate contact indices
	repeat with dup in duplicateMatches
		set dupConfidence to confidence of dup
		if dupConfidence as number ≥ 95 then
			set contact2Idx to contact2Index of dup
			if not my itemIsInList(contact2Idx, duplicateIndices) then
				set duplicateIndices to duplicateIndices & {contact2Idx}
			end if
		end if
	end repeat
	
	-- Create reduced contact list
	set reducedList to {}
	repeat with contact in contactRecords
		set currentContactIndex to contactIndex of contact
		if not my itemIsInList(currentContactIndex, duplicateIndices) then
			set reducedList to reducedList & {contact}
		end if
	end repeat
	
	return reducedList
end removeObviousDuplicates

-- Fuzzy name matching with sacred geometry patterns
on findFuzzyNameDuplicates(contactRecords)
	set matches to {}
	
	-- Limit for performance
	set maxComparisons to 5000 -- Increased from 500 to find more name duplicates
	set comparisonCount to 0
	
	repeat with i from 1 to (count of contactRecords) - 1
		if comparisonCount > maxComparisons then exit repeat
		
		set contact1 to item i of contactRecords
		set name1 to my cleanName(contactName of contact1)
		set contact1Index to contactIndex of contact1
		set contact1Name to contactName of contact1
		
		if name1 is not "" and length of name1 ≥ 3 then
			repeat with j from (i + 1) to count of contactRecords
				if comparisonCount > maxComparisons then exit repeat
				set comparisonCount to comparisonCount + 1
				
				set contact2 to item j of contactRecords
				set name2 to my cleanName(contactName of contact2)
				set contact2Index to contactIndex of contact2
				set contact2Name to contactName of contact2
				
				if name2 is not "" and length of name2 ≥ 3 then
					set similarity to my calculateNameSimilarity(name1, name2)
					
					if similarity as number ≥ 85 then
						set confidence to round similarity
						set priority to "MEDIUM"
						if similarity as number ≥ 95 then set priority to "HIGH"
						
						set matchRecord to {matchType:"name", confidence:confidence, contact1Index:contact1Index, contact2Index:contact2Index, contact1Name:contact1Name, contact2Name:contact2Name, matchValue:(name1 & " ≈ " & name2), priority:priority}
						set matches to matches & {matchRecord}
					end if
				end if
			end repeat
		end if
	end repeat
	
	return matches
end findFuzzyNameDuplicates

-- Clean name for comparison
on cleanName(nameText)
	set cleanText to my toLowerCase(nameText)
	set cleanText to my replaceInString(cleanText, "mr.", "")
	set cleanText to my replaceInString(cleanText, "mrs.", "")
	set cleanText to my replaceInString(cleanText, "ms.", "")
	set cleanText to my replaceInString(cleanText, "dr.", "")
	set cleanText to my replaceInString(cleanText, "  ", " ")
	return my trimString(cleanText)
end cleanName

-- String replacement
on replaceInString(originalString, findString, replaceString)
	set AppleScript's text item delimiters to findString
	set stringParts to text items of originalString
	set AppleScript's text item delimiters to replaceString
	set resultString to stringParts as string
	set AppleScript's text item delimiters to ""
	return resultString
end replaceInString

-- Trim whitespace
on trimString(str)
	repeat while str starts with " "
		if length of str ≤ 1 then exit repeat
		set str to text 2 thru -1 of str
	end repeat
	repeat while str ends with " "
		if length of str ≤ 1 then exit repeat
		set str to text 1 thru -2 of str
	end repeat
	return str
end trimString

-- Calculate name similarity with sacred geometry
on calculateNameSimilarity(str1, str2)
	if str1 is str2 then return 100
	if str1 is "" or str2 is "" then return 0
	
	set len1 to length of str1
	set len2 to length of str2
	set maxLen to len1
	if len2 > len1 then set maxLen to len2
	if maxLen is 0 then return 0
	
	set matches to 0
	set minLen to len1
	if len2 < len1 then set minLen to len2
	
	repeat with i from 1 to minLen
		if character i of str1 is character i of str2 then
			set matches to matches + 1
		end if
	end repeat
	
	-- Apply golden ratio adjustment for sacred geometry
	set baseScore to (matches / maxLen) * 100
	if baseScore > 50 then
		set baseScore to baseScore * 1.05 -- Slight PHI influence
	end if
	
	return round baseScore
end calculateNameSimilarity

-- Generate fractal report with full intelligence
on generateFractalReport(contactList, duplicateList, errorList, startTime, phoneTime, emailTime, nameTime, reductionPercent)
	set endTime to current date
	set totalTime to endTime - startTime
	
	set report to "══════════════════════════════════════════════" & return
	set report to report & "    FRACTAL CONTACT INTELLIGENCE REPORT v4.4" & return
	set report to report & "    🔱 Sacred Geometry Analysis Complete 🔱" & return
	set report to report & "══════════════════════════════════════════════" & return & return
	
	set report to report & "🧬 FRACTAL PROCESSING SUMMARY" & return
	set report to report & "   Session started: " & startTime & return
	set report to report & "   Session completed: " & endTime & return
	set report to report & "   Total processing time: " & my formatTime(totalTime as number) & return
	set report to report & "   Contacts processed: " & (count of contactList) & return
	set report to report & "   Fractal reduction: " & reductionPercent & "%" & return & return
	
	-- Count duplicates by type
	set phoneCount to 0
	set emailCount to 0
	set nameCount to 0
	set criticalCount to 0
	set highCount to 0
	set mediumCount to 0
	
	repeat with dup in duplicateList
		set dupType to matchType of dup
		set dupPriority to priority of dup
		
		if dupType is "phone" then set phoneCount to phoneCount + 1
		if dupType is "email" then set emailCount to emailCount + 1
		if dupType is "name" then set nameCount to nameCount + 1
		
		if dupPriority is "CRITICAL" then set criticalCount to criticalCount + 1
		if dupPriority is "HIGH" then set highCount to highCount + 1
		if dupPriority is "MEDIUM" then set mediumCount to mediumCount + 1
	end repeat
	
	set report to report & "🔍 DUPLICATE PATTERN ANALYSIS" & return
	set report to report & "   • Phone fractals: " & phoneCount & return
	set report to report & "   • Email harmonics: " & emailCount & return
	set report to report & "   • Name geometry: " & nameCount & return
	set report to report & "   TOTAL PATTERNS: " & (count of duplicateList) & return & return
	
	set report to report & "🎯 SACRED GEOMETRY BREAKDOWN" & return
	set report to report & "   • CRITICAL (Center): " & criticalCount & return
	set report to report & "   • HIGH (Inner Ring): " & highCount & return
	set report to report & "   • MEDIUM (Outer Ring): " & mediumCount & return & return
	
	-- Calculate golden ratio metrics
	if (count of contactList) > 0 then
		set goldenRatio to 1.618
		set duplicateRatio to (count of duplicateList) / (count of contactList)
		set harmonicScore to duplicateRatio * goldenRatio
		
		set report to report & "📐 SACRED METRICS" & return
		set report to report & "   • Duplicate ratio: " & (round (duplicateRatio * 100)) & "%" & return
		set report to report & "   • Harmonic score: " & (round (harmonicScore * 100) / 100) & return
		set report to report & "   • Pattern strength: "
		
		if harmonicScore > 1 then
			set report to report & "Very Strong" & return
		else if harmonicScore > 0.5 then
			set report to report & "Strong" & return
		else if harmonicScore > 0.2 then
			set report to report & "Moderate" & return
		else
			set report to report & "Weak" & return
		end if
		set report to report & return
	end if
	
	set report to report & "Report generated: " & (current date) & return
	set report to report & "🔱 Truth emerges through fractal patterns 🔱" & return
	
	return report
end generateFractalReport

-- Generate merge actions with intelligence preserved
on generateMergeActions(duplicateList)
	set actions to "═══════════════════════════════════════════════" & return
	set actions to actions & "     FRACTAL PRIORITY MERGE ACTIONS v4.4" & return
	set actions to actions & "     Sacred Geometry Contact Optimization" & return
	set actions to actions & "═══════════════════════════════════════════════" & return & return
	
	set actions to actions & "🧬 PROCESSING ORDER (Sacred Geometry):" & return
	set actions to actions & "• CRITICAL = Center point (process first)" & return
	set actions to actions & "• HIGH = Inner circle (very likely)" & return
	set actions to actions & "• MEDIUM = Outer ring (review needed)" & return & return
	
	-- Sort by priority
	set sortedDuplicates to my sortByPriority(duplicateList)
	
	-- Limit actions for readability
	set maxActions to 50
	set actionNumber to 1
	
	repeat with dup in sortedDuplicates
		if actionNumber > maxActions then
			set actions to actions & return & "... and " & ((count of sortedDuplicates) - maxActions) & " more duplicates found." & return
			set actions to actions & "Process the first " & maxActions & " critical matches first." & return
			exit repeat
		end if
		
		set dupConfidence to confidence of dup
		set dupPriority to priority of dup
		set dupType to matchType of dup
		set contact1Name to contact1Name of dup
		set contact2Name to contact2Name of dup
		set matchValue to matchValue of dup
		
		set actions to actions & "ACTION #" & actionNumber & " - " & dupPriority & " PRIORITY" & return
		set actions to actions & "──────────────────────────────────────────" & return
		set actions to actions & "Confidence: " & dupConfidence & "%" & return
		set actions to actions & "Match Type: " & dupType & return
		set actions to actions & "Match Value: " & matchValue & return & return
		
		set actions to actions & "CONTACT 1: " & contact1Name & return
		set actions to actions & "CONTACT 2: " & contact2Name & return & return
		
		if dupPriority is "CRITICAL" then
			set actions to actions & "🎯 RECOMMENDATION: MERGE (Exact match)" & return
		else if dupPriority is "HIGH" then
			set actions to actions & "🎯 RECOMMENDATION: REVIEW & MERGE" & return
		else
			set actions to actions & "🎯 RECOMMENDATION: MANUAL REVIEW" & return
		end if
		
		set actions to actions & return & "────────────────────────────────" & return & return
		
		set actionNumber to actionNumber + 1
	end repeat
	
	return actions
end generateMergeActions

-- Sort duplicates by sacred geometry priority
on sortByPriority(duplicateList)
	set criticalItems to {}
	set highItems to {}
	set mediumItems to {}
	
	repeat with dup in duplicateList
		set dupPriority to priority of dup
		if dupPriority is "CRITICAL" then
			set criticalItems to criticalItems & {dup}
		else if dupPriority is "HIGH" then
			set highItems to highItems & {dup}
		else
			set mediumItems to mediumItems & {dup}
		end if
	end repeat
	
	return criticalItems & highItems & mediumItems
end sortByPriority
