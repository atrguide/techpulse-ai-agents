# TechPulse Diagnostic Laws & Rules — Cached Reference

**Source:** Supabase tables synth_diagnostic_laws + synth_diagnostic_rules
**Cached:** 2026-05-07 — refresh by re-running pull script when laws/rules change
**Purpose:** Always-available reference so Claude Code direct path has the same diagnostic logic the synth-diagnostic-conductor uses internally — without spawning a subagent per case.

Use **short_description** for quick inline application. Pull **full_content** from Supabase only when the long form is needed.

---

## DIAGNOSTIC LAWS (29 total)

### Law #0 — The Conductor's Law *(category: global)*
A vehicle is an orchestra. Listen to the system, isolate the fault, repair the cause. Do not rebuild the stage when one instrument is out of tune.

### Law #1 — Start With What Engine Is Doing Now *(category: diagnostic_philosophy)*
Diagnose CURRENT behavior. Ignore parts history. Parts cannon history = irrelevant. Show me current fuel trims NOW.

### Law #2 — Define the DTC First *(category: diagnostic_sequence)*
Define DTC first. Use 3-7 PIDs only. Everything else is noise.

### Law #3 — Ask Questions First *(category: customer_interaction)*
Ask questions first — recent work, aftermarket parts, original complaint, timeline. Build on what they have done. Partner with the technician, do not lecture.

### Law #4 — Data Shows Problem, Schematic Finds Cause *(category: diagnostic_sequence)*
Data shows the problem, schematic finds the cause. Check power, ground, signal - in that order.

### Law #5 — Voltage and Scope Patterns Never Lie *(category: diagnostic_methodology)*
Voltage and scope patterns never lie—interpret them before replacing parts.

### Law #6 — Every Test Must Be Verifiable *(category: diagnostic_methodology)*
Every test must be verifiable. No readings without confirmation. Numbers only — no "looks good."

### Law #7 — One Step at a Time *(category: diagnostic_philosophy)*
One step at a time. Confirm each result before moving to the next. Never assume until verified — walk through the story step by step.

### Law #8 — Compare to a Known Good *(category: diagnostic_methodology)*
If something does not make sense, compare it to a known good. Known good = truth.

### Law #9 — Fuel Trims Tell the Side *(category: diagnostic_sequence)*
Fuel trims tell you the side. Scope tells you the cylinder. Use both together.

### Law #10 — CKP Sensor is the Heartbeat *(category: engine_theory)*
The CKP sensor is the heartbeat. Without the pulse, the ECM shuts down everything.

### Law #11 — Every Part Has a Purpose — Know Its Customer *(category: diagnostic_philosophy)*
Every part has a purpose. Understand what it does AND who it reports to. What system uses that data? What does the PCM do with it? Know before you test.

### Law #12 — A/F Sensors vs Rear O2 — Know the Difference *(category: diagnostic_methodology)*
A/F sensors measure mixture for fuel control. Rear O2 sensors measure catalyst oxygen storage capacity. Know which sensor does which job.

### Law #13 — Keep It Simple — Test at the Source First *(category: diagnostic_philosophy)*
Test at the source first. Do not overcomplicate when basics will tell you the answer.

### Law #14 — Use PIDs as Guidance — Verify with Scope *(category: diagnostic_methodology)*
Use PIDs as guidance but verify everything with the scope. You have to look at it RIGHT.

### Law #15 — One Bank Lean = That Bank Only *(category: diagnostic_sequence)*
One bank lean = focus on that bank. Both banks lean = focus on global systems. Don't waste time chasing the wrong side.

### Law #16 — Differential Voltage Systems Need Differential Diagnosis *(category: diagnostic_methodology)*
Differential voltage systems require differential diagnosis. Check signal high, signal low, and their difference - the PCM reads the gap, not the ground.

### Law #17 — Don't Blame the PCM First *(category: diagnostic_sequence)*
Don't blame the PCM first - but prove it wrong when it actually fails. Test sensor → wiring → PCM input → PID display.

### Law #18 — Ask Questions First When Something Is Off *(category: customer_interaction)*
When you see something off, ask questions first. Ask about recent work, aftermarket parts, original complaint, timeline. Two minutes of questions saves two days of diagnosis.

### Law #19 — Assume Nothing — Guide One Step at a Time *(category: diagnostic_philosophy)*
Assume nothing. Guide through one step at a time. Never jump ahead. Walk through the story patiently and clearly.

### Law #20 — The Compassionate Reset *(category: customer_interaction)*
Build confidence, don't make them feel stupid. "I've made mistakes too, nobody's perfect. What have you done so we don't duplicate efforts? We WILL get to the bottom of this."

### Law #21 — Test Resistance for Transmission Solenoids *(category: diagnostic_methodology)*
Test resistance, not voltage, for transmission solenoid diagnosis. Disconnect ECM, test complete circuit. Pattern reveals root cause.

### Law #22 — Handoff Discipline *(category: diagnostic_methodology)*
Don't rush the handoff. A hypothesis is allowed to be strong. A conclusion is only allowed to be earned. See it fast. Prove it slow. Call it only when the data and the test agree.

### Law #23 — Graph Before Number *(category: data_hierarchy)*
Graph before number - patterns reveal what snapshots hide.

### Law #24 — The Law of Complete Revolution Timing *(category: timing_scope)*
Timing is a relationship, not a position. Verify the complete 720 degree cycle through scope patterns before condemning components.

### Law #25 — Chrysler Differential O2 -- Raw Voltage First *(category: electrical)*
On Chrysler/Jeep/Ram differential O2 systems, check raw sensor voltage first (should be 3.0-3.3V). If voltage is wrong, the sensor is dead -- stop there. Never chase differential swing before verifying raw voltage.

### Law #26 — Universal Relay Test -- 4-Pin Systematic Method *(category: electrical)*
A relay is a relay. All relays test the same way. Test pins 30, 85, 86, 87 systematically. Never replace without testing. 2 minutes to diagnose.

### Law #27 — Track Every Verified Test -- Never Re-Ask. Never Go In Circles. *(category: diagnostic_discipline)*
Once a test result is provided and verified, it is fact. Never ask for it again. Never question it. Build on it. Every response must move the diagnosis forward.

### Law #28 — TSB First -- Check Manufacturer Knowledge Before Building Your Own Theory *(category: diagnostic_process)*
tsb-agent must return before any diagnostic output is written. A TSB exists = follow it. No result = confirmed clear to proceed.

---

## DIAGNOSTIC RULES (98 total)

### Rule Type: GENERAL

**Rule F-01 — Piezo Injector Resistance - Test Complete Circuit from ECM** *(category: fuel_injection, layer: technique)*
When testing piezo injector resistance, test from ECM connector - not at the injector. This tests the WHOLE circuit (wiring + connectors + injector) in one measurement.

**Rule F-02 — GDI Solenoid Injector Resistance - Test Complete Circuit from ECM** *(category: fuel_injection, layer: technique)*
GDI solenoid injector resistance testing. Same method as piezo - test from ECM connector to measure whole circuit. Very low resistance (under 2 ohms).

**Rule F-03 — Port Injection - Ground Pulse Testing & Bad Injector Detection** *(category: fuel_injection, layer: technique)*
Port injection is simple: 12V supply + ground pulse from ECM. The inductive kick (spike) on release tells you if the coil is healthy. No spike or weak spike = bad injector.

**Rule G-01 — Replace Guessing with Testable Steps** *(category: general, layer: governance)*
Break problems into testable yes/no questions. Simplify to basics. Replace guessing with testing.

**Rule G-02 — Simplify to Basics** *(category: general, layer: governance)*
Complexity creates confusion. Simplify problems to basic testable components: power, ground, signal.

**Rule G-03 — Confirm Each Step Before Moving Forward** *(category: general, layer: governance)*
Get specific values, not assumptions. Confirm each test result before proceeding to next step. "Did you get 12V?" not "Is power good?"

**Rule G-04 — Replicate Conditions First** *(category: general, layer: governance)*
If symptom happens under condition, duplicate it first. Test WHILE acting up. Don't assume based on experience.

**Rule G-05 — Get Second Signal for Comparison** *(category: general, layer: governance)*
If confused, get second signal. Compare crank to cam, left cam to right cam. Build pattern library for expert second opinions.

**Rule G-06 — Marathon Not Sprint - Adapt to Each Tech** *(category: general, layer: governance)*
Focus on what works FOR THAT TECH. Learn their style, work their way first, slowly introduce improvements. Marathon, not sprint.

**Rule G-07 — Cold Reset Protocol for Latched Fault Flags** *(category: general, layer: technique)*
When internal PCM fault flags latch after sensor work and standard clear fails, use cold reset protocol (battery disconnect 60+ seconds).

**Rule G-08 — PCV Leak Can Cause NEGATIVE Fuel Trims** *(category: general, layer: technique)*
A PCV system leak introduces fuel-rich crankcase vapors (not just air), causing the O2 to see rich and PCM to pull fuel. Expect negative fuel trims with low vacuum - opposite of typical vacuum leak pattern.

**Rule G-09 — Close the Learning Loop After Repair** *(category: general, layer: governance)*
After repair, confirm it fixed the problem. Document what was wrong, what fixed it, and what was learned. Every closed case builds diagnostic intelligence.

**Rule G-10 — Conflicting Data Verification Protocol** *(category: reasoning, layer: governance)*
When two data points conflict, verify measurement integrity first before interpreting either one. Do not reason about the contradiction until both measurements are confirmed valid.

**Rule G-11 — System Category Before Component Identification** *(category: reasoning, layer: governance)*
When identifying an external cause, name the system category first, then list specific components within that category. Never lead with a specific part before establishing the system.

**Rule G-12 — Handoff Discipline** *(category: reasoning, layer: governance)*
Don't rush the handoff. A hypothesis is allowed to be strong. A conclusion is only allowed to be earned. See it fast. Prove it slow. Call it only when the data and the test agree.

**Rule G-13 — Keep the Technician Engaged** *(category: general, layer: governance)*
Mechanics communicate in short bursts. Incomplete data is their natural style. Use what they gave you, name what is missing, and ask one good question that keeps the conversation moving.

**Rule G-14 — Check Your Own Work First After a Repair** *(category: general, layer: technique)*
If a new symptom appears immediately after a repair, check the repair area first. Anything disturbed, loosened, or near the work area is the primary suspect. Do not start a new diagnostic path until the completed repair has been verified.

**Rule ML-01 — Block diagnostic output until TSB check completes** *(category: general_methodology, layer: platform)*
TSB agent must return results before any diagnostic synthesis or output is surfaced.

**Rule ML-04 — Recreate dynamic conditions during voltage diagnostics** *(category: electrical, layer: technique)*
When harness disturbance appears in event history, use live voltage monitoring instead of static bench tests.

**Rule ML-06 — Present diagnostic output, not method justification** *(category: general_methodology, layer: platform)*
Ensure AI responses deliver findings and next steps, not explanations of diagnostic reasoning or rule confirmations.

**Rule ML-09 — Qualify air leak conclusions with pressure vs vacuum context** *(category: general_methodology, layer: technique)*
When smoke test is negative, avoid declaring air leak eliminated; specify test conditions and limitation.

**Rule ML-10 — Distinguish rear O2 clogging from sensor failure** *(category: sensor_diagnosis, layer: technique)*
Use rear O2 voltage + heater current to identify physical cat blockage vs chemical degradation

**Rule ML-14 — Distinguish ECM response from actual sensor failure in P0017** *(category: code_interpretation, layer: technique)*
When P0017 shows all-zero VVT scanner values, determine if zeros are ECM shutoff response or true sensor fault

**Rule ML-22 — Avoid absolute dismissals—use isolation patterns** *(category: general_methodology, layer: technique)*
When ruling out root causes, anchor reasoning to observed fault isolation patterns instead of categorical statements.

**Rule ML-32 — Recreate thermal conditions for intermittent heat faults** *(category: electrical, layer: technique)*
Apply heat stress during testing for DTCs that only appear when engine is hot or under thermal load.

**Rule ML-36 — Distinguish C1120 EPB Switch from Wheel Speed Sensor** *(category: code_interpretation, layer: technique)*
When diagnosing C1120-14, confirm it addresses EPB switch circuit, not wheel speed sensors.

**Rule ML-45 — Differentiate Dead vs Clogged Catalytic Converters by Heat Signature** *(category: sensor_diagnosis, layer: technique)*
Apply when front A/F sensors are elevated and rear O2 sensors are near zero to determine if catalyst is dead or physically clogged.

**Rule ML-46 — Verify compressor pumping before diagnosing refrigerant charge** *(category: sensor_diagnosis, layer: technique)*
Rule for AC systems: confirm pressure differential on compressor engagement before undercharge diagnosis.

**Rule ML-47 — Verify external BARO sensor location before ECM replacement** *(category: sensor_diagnosis, layer: technique)*
Always consult connector diagrams for P2227 before assuming BARO is ECM-integrated.

**Rule ML-49 — Wiggle test before condemning TPS sensors** *(category: sensor_diagnosis, layer: technique)*
When TPS dropout appears in scanner data, perform harness wiggle test to distinguish wiring faults from sensor failure.

**Rule ML-50 — Verify actual fuel level before CP4.2 diagnosis on LML Duramax** *(category: platform, layer: technique)*
When P0087 + transfer pump relay OFF + gauge reads fuel on 2015 LML Duramax, physically inspect tank before assuming pump failure.

**Rule ML-51 — Avoid premature bearing conclusions on Theta II P1326** *(category: code_interpretation, layer: technique)*
P1326 + P0017 + P0302 on Theta II engines require mechanical verification before diagnosing bearing failure.

**Rule ML-52 — Distinguish hot-crank pressure build from running pressure maintenance** *(category: fuel_system, layer: technique)*
Apply when P0087/P0191 appear during no-start or hot-soak conditions to avoid premature LPFP hypothesis.

**Rule ML-53 — Eliminate shared variables before declaring independent faults** *(category: general_methodology, layer: technique)*
Apply when multiple DTCs appear with overlapping potential root causes to avoid premature verdict language.

**Rule ML-54 — List explicit clues separately, avoid mechanism overcommitment** *(category: general_methodology, layer: technique)*
When diagnosing P0171 lean codes, enumerate ranked supporting evidence independently rather than embedding clues within a single mechanism theory.

**Rule ML-55 — Expand hypotheses when data is incomplete** *(category: general_methodology, layer: technique)*
When diagnostic data is partial or missing, broaden root cause hypotheses instead of narrowing them prematurely.

**Rule ML-56 — Scope coil primary before recommending swap tests** *(category: misfire, layer: technique)*
For misfire codes, verify tech has oscilloscope and scope coil primary waveform before recommending coil swap testing.

**Rule ML-57 — Verify Compression Test Method Before Interpreting Results** *(category: general_methodology, layer: technique)*
When compression reading contradicts crank speed, validate test procedure before diagnosing timing issues.

**Rule ML-58 — Prioritize System Category Before Specific Parts** *(category: general_methodology, layer: technique)*
When diagnosing external system causes, name the system category first before suggesting specific components.

**Rule ML-59 — Mandate spectrographic oil analysis before engine condemnation** *(category: general_methodology, layer: technique)*
Require lab oil analysis to confirm bearing wear before recommending engine replacement or goodwill claims.

**Rule ML-60 — Check turbo shaft play after control components in P0299** *(category: code_interpretation, layer: technique)*
When P0299 persists post-repair on lean-running vehicles, measure turbo shaft play after ruling out N249, N75, and wastegate actuator.

**Rule ML-61 — Anchor cylinder contribution test in misfire diagnosis** *(category: misfire, layer: technique)*
When diagnosing misfire with fuel trim and O2 sensor data, center the cylinder contribution test as the primary diagnostic anchor.

**Rule ML-62 — Verify oil pressure before diagnosing hydraulic failures** *(category: sensor_diagnosis, layer: technique)*
Don't assume oil pressure inadequacy until mechanical gauge testing confirms it first.

**Rule ML-63 — Verify control circuit before committing to mechanical failure** *(category: fuel_system, layer: technique)*
Before diagnosing mechanical wear on high-pressure fuel systems, rule out electrical/control faults causing recurrence patterns.

**Rule ML-64 — Verify Mechanical Hypothesis with Complete Waveform Data** *(category: general_methodology, layer: technique)*
Require full sensor waveforms and functional tests before naming specific mechanical wear as root cause.

**Rule ML-65 — Prioritize Platform-Specific Disables Before Contribution Tests** *(category: misfire, layer: technique)*
For DFM systems with misfire codes, test platform disable features before cylinder contribution tests.

**Rule ML-66 — Prioritize cylinder misfire over upstream O2 sensor blame** *(category: misfire, layer: technique)*
When P0301 misfire and lean codes (P0171) appear together, evaluate combustion first before attributing to O2 sensor.

**Rule ML-67 — Establish event order before assigning mechanical failure** *(category: fuel_system, layer: technique)*
When rail pressure collapses during stall, determine if pressure or control command failed first before diagnosing mechanical cause.

**Rule ML-68 — Separate hypothesis strength from conclusion certainty** *(category: general_methodology, layer: technique)*
Prevent premature diagnostic conclusions by requiring data agreement before final diagnosis calls.

**Rule ML-69 — State signal-loss conclusions with diagnostic authority** *(category: sensor_diagnosis, layer: technique)*
Assert signal event vs mechanical/fuel event directly when data supports it; don't imply.

**Rule ML-70 — Inspect ECM Connector Before PCM Replacement** *(category: general_methodology, layer: technique)*
Require physical ECM/PCM connector inspection and reseating before condemning the PCM on no-output faults.

**Rule ML-71 — Rank fuel and timing hypotheses separately before verdict** *(category: general_methodology, layer: technique)*
Apply when P0087 and P0016 appear together or fuel stall precedes sync loss.

**Rule ML-72 — Complete diagnostic output before addressing mid-task constraints** *(category: general_methodology, layer: technique)*
Never pivot to defending rule compliance mid-diagnosis; finish the diagnostic structure first.

**Rule ML-73 — Name Supporting Clues Explicitly in Ranked Diagnostics** *(category: general_methodology, layer: technique)*
Always list specific sensor values and observations as separate data points, never embedded only in narrative.

**Rule ML-74 — Distinguish hypothesis ranking from confirmation status** *(category: general_methodology, layer: technique)*
Apply when a hypothesis explains multiple findings but separator tests remain incomplete.

**Rule ML-75 — Escalate caution with incomplete diagnostic data** *(category: general_methodology, layer: technique)*
Require explicit data gaps and targeted questions when case information is intentionally or accidentally incomplete.

**Rule ML-76 — Avoid premature hypothesis closure on localized misfires** *(category: misfire, layer: technique)*
When single-cylinder misfire DTC appears with localized findings, validate systematic causes before confirming component-level root cause.

**Rule ML-77 — Always run database search before data analysis** *(category: general_methodology, layer: technique)*
Database and TSB search must precede any diagnostic analysis or conclusions on DTC cases.

**Rule ML-78 — Distinguish Loose Valve Seat from VVT System Failures** *(category: misfire, layer: technique)*
Differentiate intermittent lope with CMP dropout from mechanical VVT issues using load response patterns.

**Rule ML-79 — Eliminate fuel pressure checks for one-bank lean conditions** *(category: lean_rich, layer: technique)*
Skip fuel pressure testing when only one bank shows lean; problem is bank-specific, not fuel system-wide.

**Rule ML-80 — Distinguish hypothesis from confirmed diagnosis** *(category: general_methodology, layer: technique)*
Prevent presenting diagnostic hypotheses as confirmed causes without physical verification.

**Rule ML-81 — Distinguish hypothesis from confirmed diagnosis** *(category: general_methodology, layer: technique)*
Do not declare root cause confirmed until physical inspection and post-repair verification are complete.

**Rule ML-82 — Always check TSB before diagnosing battery-related codes** *(category: general_methodology, layer: technique)*
Run TSB/software update search before final diagnosis on any vehicle, especially after battery service.

**Rule ML-83 — Verify sensor type before diagnosing fuel trim faults** *(category: sensor_diagnosis, layer: technique)*
When P0171 + P0505 appear together, confirm actual sensor installed matches ECM expectation before assuming sensor failure.

**Rule ML-84 — Distinguish Live Diagnostic Cases from Simulated Test Data** *(category: general_methodology, layer: technique)*
Apply real-world diagnostic protocols when cases originate from live shop vehicles, not simulation environments.

**Rule ML-85 — Apply O2 Direction Filter Before Cause Evaluation** *(category: lean_rich, layer: technique)*
Use O2 reading direction as a diagnostic gate to eliminate mismatched causes immediately.

**Rule ML-86 — Prioritize vacuum leaks for sudden-onset P0171 + idle surge** *(category: lean_rich, layer: technique)*
When P0171 lean + idle surge + multi-cylinder misfire appear suddenly, inspect PCV hose and vacuum system before electrical paths.

**Rule ML-87 — Verify Module Location Before U3000-49 Diagnosis** *(category: code_interpretation, layer: technique)*
Always confirm which module stores U3000-49 before diagnosing; code appears across SRS, ADAS, BCM, and other modules.

**Rule RULE_01 — Explain Only What Is Needed to Get to the Next Step** *(category: general, layer: governance)*
Give technicians one step at a time without overwhelming. Sequential, focused guidance beats information dumps.

**Rule RULE_02 — Ask What They Already Did Before Giving a Solution** *(category: general, layer: governance)*
Always ask for diagnostic history before recommending next steps to avoid duplicating effort and build on technician work.

**Rule RULE_03 — If They Are Guessing, Break It Into Testable Steps** *(category: general, layer: governance)*
When a technician is guessing, give a systematic sequence of testable steps with reasoning. Teach system relationships, not just procedures.

**Rule RULE_04 — When Unsure, Simplify to the 6 Basics** *(category: general, layer: governance)*
When a technician is completely lost, return to the 6 engine basics: fuel, spark, air, compression, timing, signals.

**Rule RULE_05 — Use Schematic Diagnosis to Isolate - Never Guess a Module** *(category: general, layer: governance)*
Verify all external factors (power, ground, inputs) before condemning a module. Never guess a module is bad.

**Rule RULE_06 — Let the Data Speak First** *(category: general, layer: governance)*
Review live data, freeze frame, and scope patterns before drawing conclusions from codes alone. Always reset KAM after repairs.

**Rule RULE_07 — Always Go One Step at a Time - Ask for Confirmation Before Drawing Conclusions** *(category: general, layer: governance)*
Confirm each diagnostic step with specific values before proceeding. After repair, ask if it worked and document the outcome for the case study database.

**Rule RULE_08 — If the Symptom Happens Under a Condition, Duplicate It First** *(category: general, layer: governance)*
Replicate the conditions that cause the symptom before testing. Catch failures in the act. Never assume based on experience without replicating.

**Rule RULE_09 — If There Is Confusion, Get a Second Signal** *(category: general, layer: governance)*
Capture additional signals for comparison when a pattern is uncertain. Build and use a pattern library to provide expert second opinions.

**Rule RULE_10 — When a Tech Is Stuck, Focus on What Works for That Tech** *(category: general, layer: governance)*
Learn each technician style and work within it. Meet them where they are.

**Rule RULE_11 — Cold Reset Protocol - When Internal Fault Flags Latch After Sensor Work** *(category: general, layer: governance)*
When codes return immediately after verified good installation, disconnect 12V battery 60+ seconds to force complete PCM reboot and clear internal fault flags.

**Rule RULE_12 — Test the Complete Circuit, Not Just the Part** *(category: general, layer: governance)*
Keep component connected, break at the control side. Test the circuit as a system.

**Rule RULE_13 — Sudden Drop = Electrical, Gradual Drop = Mechanical** *(category: reasoning, layer: governance)*
The shape of sensor data change reveals the nature of the failure.

**Rule RULE_PDF_LAW_REF — Law References in PDF Diagnostic Reports - Reference Only, Do Not Reproduce** *(category: general, layer: platform)*
In PDF diagnostic reports, reference laws by number and title only. Do not copy full law text, case studies, or footnotes. Laws are the master reference; PDFs show case application.

**Rule V-01 — GM 1.5L Turbo (LYX/LE2/L3A) - Non-Applicable PIDs** *(category: vehicle_specific, layer: platform)*
DO NOT CHASE: MAF Supply Voltage Command=OFF, 5V Reference 5=0V, MAF Circuit Open=MALFUNCTION on GM 1.5L Turbo.
  These display false readings on known good vehicles.

### Rule Type: SCOPE

**Rule SCOPE_R_S1 — Always Verify Reference Before Signal** *(category: scope, layer: technique)*
Verify power and ground at sensor before analyzing waveform patterns. Bad power or ground makes signal analysis meaningless.

**Rule SCOPE_R_S10 — MAP Sensor Relative Compression Test** *(category: scope, layer: technique)*
Scope MAP sensor voltage synced to cylinder 1 ignition trigger to identify weak cylinders via vacuum signature without removing spark plugs.

**Rule SCOPE_R_S2 — Think in 720 Degrees - One Cylinder, One Complete Cycle** *(category: scope, layer: technique)*
Set scope timebase to capture 720 degrees (one complete 4-stroke cycle) to reveal timing relationships, fuel delivery, ignition events, and misfire causes.

**Rule SCOPE_R_S3 — A Sensor Must Swing Both Directions - Verify High AND Low** *(category: scope, layer: technique)*
Verify a sensor responds in both directions (rich and lean, high and low). A sensor stuck in one direction appears to work but is actually failed.

**Rule SCOPE_R_S4 — If It Looks Good, Move On - Do Not Chase Perfection** *(category: scope, layer: technique)*
When a pattern shows proper amplitude, expected frequency, clean transitions, and no obvious faults, document it and move to the next sensor. Do not analyze healthy waveforms for microscopic imperfections.

**Rule SCOPE_R_S5 — Overlay a Known Good Pattern Every Chance You Can** *(category: scope, layer: technique)*
Compare problem patterns to known-good patterns from another vehicle, a library reference, or a good cylinder on the same engine to instantly reveal defects.

**Rule SCOPE_R_S6 — Use Frequency Measurement to See Flow and Cycling Rates** *(category: scope, layer: technique)*
Use the Hz button on the scope to measure MAF airflow rates, solenoid cycling frequencies, and PWM duty cycles - a powerful underutilized diagnostic tool.

**Rule SCOPE_R_S7 — A Flat Trace Needs Power AND Ground Verified - Not Just Voltage** *(category: scope, layer: technique)*
When scope shows flat line, verify both power source AND ground return path. Voltage everywhere with no signal means no ground - not a bad component.

**Rule SCOPE_R_S8 — Verify the Fix - Capture Before AND After Patterns** *(category: scope, layer: technique)*
Capture waveform patterns before and after repair to prove the fix worked, document case studies, and build the pattern library.

**Rule SCOPE_R_S9 — Noise Repeating with Firing Frequency Equals Shared Ground Return** *(category: scope, layer: technique)*
When noise on a sensor signal repeats synchronized to engine cylinder firing frequency, it indicates a shared ground return path between the sensor and a high-current circuit.

**Rule TIMING_SCOPE_LAW_1 — 720 Degree Reference Window - All Timing Diagnoses Must Use This Window** *(category: timing, layer: technique)*
Establish a 720-degree reference window using injector or ignition trigger as scope trigger. All cam, crank, and VVT signals must be compared within this consistent window.

**Rule TIMING_SCOPE_LAW_2 — Cam/Crank Correlation - Cam Edge Must Align at Specific Crank Pattern Positions** *(category: timing, layer: technique)*
Within the 720-degree window, cam sensor transition edges must align at specific crank pattern positions. Misalignment proves jumped timing without engine teardown.

**Rule TIMING_SCOPE_LAW_3 — Cam/Cam Correlation - Compare All Four Cam Sensors to Find Which Cam Jumped** *(category: timing, layer: technique)*
Capture all four cam sensors simultaneously within 720-degree window. Spatial misalignment of one cam relative to others precisely identifies which bank and camshaft jumped timing.

**Rule TIMING_SCOPE_LAW_4 — VVT/Phaser Testing Law - Variable Valve Timing Diagnostic Procedure** *(category: timing, layer: technique)*
Diagnose VVT phaser operation by capturing solenoid command and cam sensor response to distinguish electrical failure vs mechanical phaser failure without valve cover removal.

**Rule TIMING_SCOPE_PROC — Timing Scope Diagnostic Procedure - Quick Reference Decision Tree** *(category: timing, layer: technique)*
Quick reference decision tree for scope timing projects. Running engine: check crank/cam sync PID first. No-start: do cam/crank correlation first, then cam/cam.
