from corr_map import corr_map

# Consts

rest_path = '../../fMRI Data for Tutorial and HW/resting_group2_reg/'
task_path = '../../fMRI Data for Tutorial and HW/story_selected_reg_wm_csf_hsd_last_half2/'
PCC_VOI_path ='../../fMRI Data for Tutorial and HW/DMN_PREC_ROI.voi'
AUDITORY_VOI_path='../../fMRI Data for Tutorial and HW/a1_group2_new.voi'
nii_path = '../../fMRI Data for Tutorial and HW/MNI152_T1_3mm_brain.nii'

# PCC
corr_map(rest_path, nii_path, PCC_VOI_path, 1, 1, 'py_1pcc_rest_fc_')
corr_map(rest_path, nii_path, PCC_VOI_path, 1, 0, 'py_2pcc_rest_isfc_')
corr_map(task_path, nii_path, PCC_VOI_path, 1, 1, 'py_3pcc_task_fc_')
corr_map(task_path, nii_path, PCC_VOI_path, 1, 0, 'py_4pcc_task_isfc_')

# Early Auditory Area - Auditory Network
corr_map(task_path, nii_path, AUDITORY_VOI_path, 1, 1, 'py_5eae_task_fc_')
corr_map(task_path, nii_path, AUDITORY_VOI_path, 1, 0, 'py_6eae_task_isfc_')
corr_map(task_path, nii_path, AUDITORY_VOI_path, 5, 1, 'py_7eae_task_fc_')
corr_map(task_path, nii_path, AUDITORY_VOI_path, 5, 0, 'py_8eae_task_isfc_')