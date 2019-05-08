import os
import matlab.engine

result_file = 'result_summary.csv'
faulty_scenario = [1,2,3,4,5,6,7,8]
#total_scenario = 8
total_scenario = len(faulty_scenario)
scene_ind = 0; fault_ind = 1; alert_ind = 3; hazard_ind = 4; t1_ind = 5; t2_ind = 6; t3_ind = 7
total_fault = 0
total_alert = 0.0
total_hazard = 0.0
h1_hazard = 0.0
h2_hazard = 0.0
h3_hazard = 0.0
h3h1_hazard = 0.0
alert_FN = 0.0
alert_FP = 0.0

time_alert = []
time_hazard = []
time_react = []
time_manifest = []
time_safe = []
scene_fault = []
scene_alert = []
scene_hazard = []
numHz = 0
numAl = 0
scenario = 1
scene_al = 0.0
scene_hz = 0.0
scene_react = 0.0
scene_manifest = 0.0
scene_safe = 0.0
altime = 0.0
hztime = 0.0
reactime = 0.0
mnftime = 0.0
sftime = 0.0
temp_timeHz = 0.0
temp_timeAl = 0.0
total_hazard_time = 0.0
total_alert_time = 0.0
total_react_time = 0.0
total_manifest_time = 0.0
total_safe_time = 0.0
total_react = 0.0
total_manifest = 0.0
total_safe = 0.0

manifest_time = []
safe_time = []

mnf_alert = 0.0
total_mnf_alert = 0.0
mnf_hazard = 0.0
total_mnf_hazard = 0.0
mnf_safe = 0.0
total_mnf_safe = 0.0
alert_safe = 0.0
total_alert_safe = 0.0

activated = 0
with open(result_file, 'r') as readfile:
    readfile.readline()
    tmp_fault = 0
    for line in readfile:
        total_fault += 1
        tmp_fault += 1.0

        line_seg = line.split(',')
        ind_offset = len(line_seg)-8
        if 'N/A' in line_seg[t1_ind + ind_offset]:
        # if manifest_time[total_fault-1] < 0.:
          continue
        activated += 1


        if 'N/A' not in line_seg[alert_ind + ind_offset]:
            total_alert += 1.0
            if 'N/A' in line_seg[hazard_ind + ind_offset]:
                alert_FP += 1.0
        else:
            if 'N/A' not in line_seg[hazard_ind + ind_offset]:
                alert_FN += 1.0

        if 'N/A' not in line_seg[hazard_ind + ind_offset]:
            total_hazard += 1.0

            if 'H1' in line_seg[hazard_ind + ind_offset]:
                h1_hazard += 1.0
            elif 'H2' in line_seg[hazard_ind + ind_offset]:
                h2_hazard += 1.0
            # elif 'H3' in line_seg[hazard_ind + ind_offset]:
            #     h3_hazard += 1.0

        if scenario != int(line_seg[scene_ind]):
            scene_alert.append(numAl)
            scene_hazard.append(numHz)
            numAl=0
            numHz=0
            if altime > 0.0:
                time_alert.append(altime/scene_al)
                altime = 0.0
                scene_al = 0.0
            else:
                time_alert.append(-1.0)

            if hztime > 0.0:
                time_hazard.append(hztime/scene_hz)
                hztime = 0.0
                scene_hz = 0.0
            else:
                time_hazard.append(-1.0)

            if reactime > 0.0:
                time_react.append(reactime/scene_react)
                reactime = 0.0
                scene_react = 0.0
            else:
                time_react.append(-1.0)

            # if mnftime > 0.0:
            #     time_manifest.append(mnftime/scene_manifest)
            #     mnftime = 0.0
            #     scene_manifest = 0.0
            # else:
            #     time_manifest.append(-1.0)

            # if sftime > 0.0:
            #     time_safe.append(sftime/scene_safe)
            #     sftime = 0.0
            #     scene_safe = 0.0
            # else:
            #     time_safe.append(-1.0)

            scenario = int(line_seg[scene_ind])
            scene_fault.append(tmp_fault)
            tmp_fault = 0.0

        if 'N/A' not in line_seg[alert_ind + ind_offset]:
            if '||' not in line_seg[alert_ind + ind_offset]:
                temp_timeAl = float(line_seg[t2_ind + ind_offset])
            else:
                tmp_line = line_seg[t2_ind + ind_offset].split('||')
                temp_timeAl = float(tmp_line[0])
            altime += abs(temp_timeAl - float(line_seg[t1_ind + ind_offset]))
            total_alert_time += abs(temp_timeAl - float(line_seg[t1_ind + ind_offset]))
            scene_al += 1.0
            numAl += 1

        if 'N/A' not in line_seg[hazard_ind + ind_offset]:
            if '||' not in line_seg[hazard_ind + ind_offset]:
                temp_timeHz = float(line_seg[t3_ind + ind_offset])
            else:
                tmp_line = line_seg[t3_ind + ind_offset].split('||')
                temp_timeHz = float(tmp_line[0])
            hztime += temp_timeHz - float(line_seg[t1_ind + ind_offset])
            total_hazard_time += temp_timeHz - float(line_seg[t1_ind + ind_offset])
            scene_hz += 1.0
            numHz += 1
            if 'N/A' not in line_seg[alert_ind + ind_offset]:
                if temp_timeHz >= temp_timeAl:
                    reactime += temp_timeHz - temp_timeAl
                    total_react_time += temp_timeHz - temp_timeAl
                    total_react += 1.0
                    scene_react += 1.0
        # else:
        #     if safe_time[total_fault-1]>-1.0:   ## -1 means not manifested, so no need to calculate these time values
        #         sftime += (safe_time[total_fault-1] - float(line_seg[t1_ind+ind_offset]))
        #         total_safe_time += (safe_time[total_fault-1] - float(line_seg[t1_ind+ind_offset]))
        #         total_safe += 1.0
        #         scene_safe += 1.0
        #         if 'N/A' not in line_seg[alert_ind + ind_offset]:
        #             alert_safe += abs(temp_timeHz - safe_time[total_fault - 1])
        #             total_alert_safe += 1.0

                # if manifest_time[total_fault - 1] < 30.0:
                #     mnf_safe += abs(manifest_time[total_fault-1] - safe_time[total_fault - 1])
                #     total_mnf_safe += 1.0

        # if manifest_time[total_fault-1] < 30.0:
        #     mnftime += (manifest_time[total_fault-1] - float(line_seg[t1_ind+ind_offset]))
        #     total_manifest_time += (manifest_time[total_fault-1] - float(line_seg[t1_ind+ind_offset]))
        #     total_manifest += 1.0
        #     scene_manifest += 1.0
        #     if 'N/A' not in line_seg[hazard_ind + ind_offset]:
        #         mnf_hazard += temp_timeHz - manifest_time[total_fault-1]
        #         total_mnf_hazard += 1.0

        #     if 'N/A' not in line_seg[alert_ind + ind_offset]:
        #         mnf_alert += abs(temp_timeAl - manifest_time[total_fault-1])
        #         total_mnf_alert += 1.0


    scene_alert.append(numAl)
    scene_hazard.append(numHz)
    numAl=0
    numHz=0
    if altime > 0.0:
        time_alert.append(altime / scene_al)
    else:
        time_alert.append(-1.0)

    if hztime > 0.0:
        time_hazard.append(hztime / scene_hz)
    else:
        time_hazard.append(-1.0)

    if reactime > 0.0:
        time_react.append(reactime / scene_react)
    else:
        time_react.append(-1.0)

    # if mnftime > 0.0:
    #     time_manifest.append(mnftime/scene_manifest)
    # else:
    #     time_manifest.append(-1.0)

    # if sftime > 0.0:
    #     time_safe.append(sftime / scene_safe)
    # else:
    #     time_safe.append(-1.0)

    scene_fault.append(tmp_fault)

    with open('result_analysis/output_analysis.txt', 'w') as outfile:
        outfile.write('Total number of faults: ' + str(int(total_fault)) + '\n')
        # outfile.write('Total number of manifested faults: ' + str(int(total_manifest)) + '\n')
        outfile.write('Alerts: %.2f %% (total: %d)\n' % (100.0 * total_alert / total_fault, total_alert))
        outfile.write('Hazards: %.2f %% (total: %d)\n' % (100.0 * total_hazard / total_fault, total_hazard))
        outfile.write('Hazards (H1 only): %.2f %%\n' % (100.0 * h1_hazard / total_hazard))
        outfile.write('Hazards (H2 only): %.2f %%\n' % (100.0 * h2_hazard / total_hazard))
        # outfile.write('Hazards (H3 only): %.2f %%\n' % (100.0 * h3_hazard / total_hazard))
        # outfile.write('Hazards (H1 and H3): %.2f %%\n' % (100.0 * h3h1_hazard / total_hazard))
        outfile.write('Alerts showed up but no Hazard: %d \n' % alert_FP)
        outfile.write('Alerts False Positive: %.2f %%\n' % (100.0 * alert_FP / (total_fault - total_hazard)))
        outfile.write('Alerts did not show up but Hazards occurred: %d \n' % alert_FN)
        outfile.write('Alerts False Negative: %.2f %%\n' % (100.0 * alert_FN / total_hazard))
        outfile.write('Average alert time: %.4fs \n' % (total_alert_time/total_alert))
        outfile.write('Average time to hazard: %.4fs \n' % (total_hazard_time/total_hazard))
        # outfile.write('Average time to react: %.4fs \n' % ((mnf_hazard/ total_mnf_hazard)-(mnf_alert / total_mnf_alert)))
        # outfile.write('Average time to manifest: %.4fs \n' % (total_manifest_time/total_manifest))
        # outfile.write('Average time to safe state: %.4fs \n' % (total_safe_time / total_safe))
        # outfile.write('Average time from manifest to hazard: %.4fs \n' % (mnf_hazard/ total_mnf_hazard))
        # outfile.write('Average time from manifest to alert: %.4fs \n' % (mnf_alert / total_mnf_alert))
        # outfile.write('Average time from manifest to safe state: %.4fs \n' % (mnf_safe / total_mnf_safe))
        # outfile.write('Average time from alert to safe state: %.4fs \n' % (alert_safe / total_alert_safe))
        outfile.write('Total number of activated faults: ' + str(int(activated)) + '\n')



    with open('result_analysis/time_analysis.csv', 'w') as outfile:
        outfile.write('Scenario, Total fault, Total alerts, Total hazards, Average alert time, Average hazard time, Average reaction time, Average manifest time, Average safe state time \n')
        for i in range(0, total_scenario):
            if time_alert[i] > -1.0:
                altime = str(time_alert[i])
            else:
                altime = 'N/A'

            if time_hazard[i] > -1.0:
                hztime = str(time_hazard[i])
            else:
                hztime = 'N/A'

            if time_react[i] > -1.0:
                #reactime = str(time_react[i])
                reactime = str(time_hazard[i]-time_alert[i])
            else:
                reactime = 'N/A'

            # if time_manifest[i] > -1.0:
            #     mnftime = str(time_manifest[i])
            # else:
            #     mnftime = 'N/A'

            # if time_safe[i] > -1.0:
            #     sftime = str(time_safe[i])
            # else:
            #     sftime = 'N/A'

            outfile.write('%d, %d, %d, %d, %s, %s, %s, %s, %s \n' \
                          % (faulty_scenario[i], scene_fault[i], scene_alert[i], scene_hazard[i], altime, hztime, reactime,"",""))#, mnftime, sftime))


#print time_alert
#print time_hazard
#print time_react

print total_safe
print activated

