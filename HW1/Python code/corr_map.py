import glob
import warnings
import numpy as np
from scipy.io import loadmat
from nilearn.image import load_img, coord_transform
import nibabel as nib
from brainvoyagertools.voi import VOIsDefinition as voi_reader

warnings.filterwarnings("ignore")


def corr_map(fMRI_folder_path, nii_path, VOI_path, select_voi=1, method=1, name=''):
    # find FMRI data and load nifti and VOI file
    fmri_data_path = fMRI_folder_path
    fmri_files = sorted(glob.glob(fmri_data_path+'*.mat'))  # load fMRI data - mat files
    fmri_avg_files = sorted(glob.glob(fmri_data_path+'avg/*.mat'))  # load average fMRI data - mat files
    if (len(fmri_avg_files) != 18) and (len(fmri_files) != 18):
        print("Can't load files, please check fMRI folder path")
    try:
        ROI_template = load_img(nii_path)
    except ValueError:
        print("Can't load files, please check nii path")
    try:
        voi = voi_reader(load=VOI_path)
    except OSError:
        print("Can't load files, please check VOI path")

    inv_affine_mat = np.linalg.inv(ROI_template.affine)
    voxels = []
    for x, y, z in voi.vois[select_voi-1].data:
        x_vox, y_vox, z_vox = coord_transform(x, y, z, inv_affine_mat)
        voxels.append(np.round((x_vox, y_vox, z_vox)).astype(int))
    voxels = np.array(voxels)

    roi = np.zeros(ROI_template.shape, dtype=int)
    for voxel in voxels:
        roi[voxel[0], voxel[1], voxel[2]] = 1

    roimask = roi.flatten('F')

    # Consts for correlation map
    Nsub = 18  # number of subjects = 18
    Nsamp = 280  # TR
    threshold = 6000  # signal threshold

    # create correlation map
    for subject in range(1, Nsub + 1):
        print(f'Analysis Subject {subject}')
        bold_one_temp = loadmat(fmri_files[subject - 1])['data_crop'].T

        if subject == 1:
            Nsamp, Nvox = bold_one_temp.shape
            csub_2 = np.empty((Nvox, Nsub))
            csub_2[:] = np.NaN

        mask_single = np.mean(bold_one_temp, axis=0) > threshold

        bold_one_temp[:, ~mask_single] = np.NaN

        ROI = bold_one_temp[:, roimask.astype(bool)]

        ROI_norm = (ROI - np.mean(ROI, axis=0)) / np.std(ROI, axis=0)

        B = np.nanmean(ROI_norm, axis=1)

        if method == 1:
            gg_avg = np.where(mask_single)[0]
            Ng_avg = len(gg_avg)
            B_avg = bold_one_temp[:Nsamp, gg_avg]
        else:
            bold_avg = loadmat(fmri_avg_files[subject - 1])['bold_avg']
            mask_avg = bold_avg[-1, :]
            bold_avg = bold_avg[:-1, :][:Nsamp, :]

            gg_avg = np.where(mask_avg)[0]
            Ng_avg = len(gg_avg)
            B_avg = bold_avg[:, gg_avg]

        B = (B - np.mean(B)) / (np.sqrt(Nsamp - 1) * np.std(B))

        B_avg = (B_avg - np.mean(B_avg, axis=0)) / (np.sqrt(Nsamp - 1) * np.std(B_avg, axis=0))

        cc = B_avg.T @ B
        csub_2[gg_avg, subject - 1] = cc

    # save corrlation map
    method_name = ['ISFC', 'FC']

    avg_map_dmn = np.nanmean(csub_2, axis=1)
    mean_corr_img = np.reshape(avg_map_dmn, (61, 73, 61), order='F')
    print('Saving maps')

    nii = nib.load(nii_path)
    nii_data = nii.get_fdata()
    nii_data[np.isnan(nii_data)] = 0
    nii_updated = nib.Nifti1Image(mean_corr_img, nii.affine, nii.header)

    save_name = f'{name}CorrelationMap_{method_name[method]}_ROI_{select_voi}.nii'
    nib.save(nii_updated, save_name)
    print(f'Saved {save_name}')
