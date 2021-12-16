# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt
import numpy as np

from numpy import random
from scipy.interpolate import griddata

#----------------------UNIVERSAL PLOTTING FUNCTIONS---------------------------# 
###############################################################################
"""Plots Fast Fourier Transform"""
def plot_fft(f, ss1, idf):
    plt.figure()
    plt.plot(f, ss1, 'k-', linewidth = 0.5)
    plt.ylabel('|FFT(signal)|')
    plt.xlabel('f [Hz]')
    plt.text(0.8*np.max(f), 0.9*np.max(ss1), 'signal: '+str(idf), fontsize=12)
    
"""Plots modes in 3D"""
def plot_modes_3d(xco, yco, data, cmp, nmodes):
    # set the figure parameters
    fig = plt.figure()
    for i in range(nmodes):
        sub = fig.add_subplot(4, 2, i+1, projection='3d')
        sub.set_title('mode ' + str(i+1))
        sub.plot_surface(xco.T, yco.T, np.reshape(data[:,i], (120, 320), order='F'),
                        cmap=cmp, linewidth=0)
        plt.show()

"""Compares reconstructed snapshot with raw snashot from data"""
def plot_visual_inspect(data, rdata, row, col, cmp):
    # pick a random snapshot from range
    snap = random.randint(np.size(data, axis=1))
    # set the figure parameters
    fig = plt.figure(figsize=(10, 3))
    
    # figure 1 X - real data
    sub = fig.add_subplot(1, 2, 1)
    sub.set_title('Raw data, snap ' + str(snap))
    img = sub.imshow(np.reshape(data[:,snap], (row, col), order='F'), origin='upper', cmap=cmp)
    
    # figure 2 Xdmd - reconstructed data
    sub = fig.add_subplot(1, 2, 2)
    sub.set_title('Reconstructed, snap ' + str(snap))
    img = sub.imshow(np.reshape(rdata[:,snap], (row, col), order='F'), origin='upper', cmap=cmp)
    
    fig.colorbar(img, fraction=0.02, pad=0.05, extend='both', orientation='vertical')
    fig.tight_layout()

"""Visualizes the MAPE error"""
def error_visualizer(x, xmod, mape):
    # visualization of an error
    plt.figure()
    plt.scatter(xmod, x, s = 0.05, c = 'black')
    plt.text(np.max(xmod)-np.mean(xmod), np.min(x), r'MAPE: ' + str(round(mape,2)) + '[%]', fontsize=12)
    plt.xlabel('Reconstructed Ux [m/s]')
    plt.ylabel('Reference Ux [m/s]')

#----------------------GRIDED DATA PLOTTING FUNCTIONS-------------------------# 
###############################################################################
"""This plotting function is used when is necessary to plot grided data. The
   ploting function is universal for POD and DMD analysis. If thorough analysis
   is done, additional features should be added to function."""
def plot_modes_grided(data, row, col, cmp, nmodes):
    # set the figure parameters
    fig = plt.figure(dpi=150)
    for i in range(nmodes):
        sub = fig.add_subplot(2, 4, i+1)
        sub.set_title('mode ' + str(i+1))
        img = sub.imshow(np.reshape(data[:,i], (row, col), order='F'), origin='upper',
                    cmap=cmp)
        sub.set_xticks(np.arange(1, col+col/10, step=col/9))  # Set label locations.
        sub.set_xticklabels(['-1','0','1','2','3','4','5','6','7','8'])
        
        sub.set_yticks(np.arange(1, row+row/5, step=row/4))  # Set label locations.
        sub.set_yticklabels(['2','1','0','-1','-2'])  # Set text labels..
        # size1 = 10
        # size2 = 10
        # size3 = 10
        # plt.rc('axes', titlesize=size1)     # fontsize of the axes title
        # plt.rc('axes', labelsize=size3)    # fontsize of the x and y labels
        # plt.rc('xtick', labelsize=size2)    # fontsize of the tick labels
        # plt.rc('ytick', labelsize=size2)    # fontsize of the tick labels
    fig.add_subplot(111, frameon=False)
    # hide tick and tick label of the big axis
    plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
    plt.xlabel("X [m]")
    plt.ylabel("Y [m]")
    fig.subplots_adjust(right=0.85)
    plt.subplots_adjust(top=0.965, bottom=0.095, left=0.085, right=0.83, hspace=0.2, wspace=0.15)

    cbar_ax = fig.add_axes([0.85, 0.28, 0.01, 0.5])
    cbar = plt.colorbar(img, cax=cbar_ax, extend='both', orientation='vertical')
    cbar.set_label(R"$\phi_i(\xi)$ [-]")
            
#---------------------SCATTERED DATA PLOTTING FUNCTIONS-----------------------# 
###############################################################################
"""This plotting function is used when is necessary to plot scattered data. The
   ploting function is universal for POD and DMD analysis. If thorough analysis
   is done, additional features should be added to function."""
def plot_modes_sct(xco, yco, data, cmp, nmodes):
    # set the figure parameters
    fig = plt.figure()
    fig.suptitle('Dominant POD modes')
    for i in range(nmodes):
        sub = fig.add_subplot(4, 2, i+1)
        sub.set_title('mode ' + str(i+1))
        img = plt.scatter(xco, yco, c = data[:,i], s=1, cmap=cmp)
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.01, 0.7])
    cbar = plt.colorbar(img, cax=cbar_ax, extend='both', orientation='vertical')
    cbar.set_label(R"$\phi(\xi)$ [-]")

#-----------------PLOTTING FUNCTIONS FOR POD ANALYSIS-------------------------# 
###############################################################################
"""Following functions are specifically designed and optimized for the purposes
   of the Master Thesis. If applied to a diefferent data set, or example, one 
   it should be closely examined if provided functions fulfill requirements of
   performed analysis."""
def plot_pod_avg_vel(data, coor, cmp):
    xmin = np.min(coor[:,0])
    xmax = np.max(coor[:,0])
    ymin = np.min(coor[:,1])
    ymax = np.max(coor[:,1])
    row, col = np.mgrid[ymin:ymax:120j, xmin:xmax:320j]
    fig = plt.figure()
    fig.suptitle('Average Velocity Field')
    intp = griddata(coor, data, (col, row), method='linear')
    img = plt.imshow(intp, origin='upper', cmap=cmp, extent=[xmin, xmax, ymin, ymax])
    fig.colorbar(img, fraction=0.02, pad=0.05, extend='both', orientation='vertical')
    
def plot_pod_modes_imgip(data, coor, cmp, nmodes):
    # set the figure parameters
    xmin = np.min(coor[:,0])
    xmax = np.max(coor[:,0])
    ymin = np.min(coor[:,1])
    ymax = np.max(coor[:,1])
    row, col = np.mgrid[ymin:ymax:120j, xmin:xmax:320j]
    fig = plt.figure()
    fig.suptitle('Dominant POD modes')
    for i in range(nmodes):
        intp = griddata(coor, data[:,i], (col, row), method='linear')
        sub = fig.add_subplot(4, 2, i+1)
        sub.set_title('mode ' + str(i+1))
        img = sub.imshow(intp, origin='upper', cmap=cmp, extent=[xmin, xmax, ymin, ymax],
                         vmin = -0.05, vmax = 0.05)
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.01, 0.7])
    cbar = plt.colorbar(img, cax=cbar_ax, extend='both', orientation='vertical')
    cbar.set_label(r"$\phi(\xi)$ [-]")

def plot_variance_pod(eigs, nmodes):
    var = np.cumsum(eigs[0:nmodes])/np.sum(eigs)
    print('Variance preserved: ' + str(round(var[-1]*100, 3)) + ' %')
    modes = np.arange(1,nmodes+1,1)
    fig, axs = plt.subplots(1, 1, dpi=150)
    # plot 1
    # axs[0].plot(modes, eigs[0:nmodes], 'k-', linewidth=0.5) 
    # axs[0].plot(modes, eigs[0:nmodes], 'r.')
    # axs[0].set_ylabel('Variance [%]')
    # axs[0].set_xlabel('Mode')
    # plot 2
    # axs[1].plot(modes, var, 'k-', linewidth=0.5)
    # axs[1].plot(modes, var, "r.")
    # axs[1].set_ylabel('Variance [%]')
    # axs[1].set_xlabel('Mode')
    plt.plot(modes, var*100, 'k-', linewidth=0.5)
    plt.plot(modes, var*100, "r.")
    plt.ylabel('Variance [%]')
    plt.xlabel('Mode')
    fig.tight_layout()
    plt.show()

#-----------------PLOTTING FUNCTIONS FOR DMD ANALYSIS-------------------------# 
###############################################################################
"""Following functions are specifically designed and optimized for the purposes
   of the Master Thesis. If applied to a diefferent data set, or example, one 
   it should be closely examined if provided functions fulfill requirements of
   performed analysis."""
def plot_dmd_modes_imgip_vi(data, coor, cmp, nmodes):
    # set the figure parameters
    if len(nmodes) %2 == 0:
        print(str(len(nmodes))+' is even!')
    else:
        print(str(len(nmodes))+' is odd!')
    r = int(input('Rows: '))
    c = int(input('Columns: '))
    xmin = np.min(coor[:,0])
    xmax = np.max(coor[:,0])
    ymin = np.min(coor[:,1])
    ymax = np.max(coor[:,1])
    row, col = np.mgrid[ymin:ymax:120j, xmin:xmax:320j]
    fig = plt.figure()
    for i in range(len(nmodes)):
        intp = griddata(coor, data[:,nmodes[i]], (col, row), method='linear')
        sub = fig.add_subplot(r, c, i+1)
        sub.set_title('mode ' + str(nmodes[i])+'('+str(1+i)+')')
        sub.imshow(intp, origin='upper', cmap=cmp, extent=[xmin, xmax, ymin, ymax],
                         vmin = -0.05, vmax = 0.05)

def plot_dmd_modes_imgip(data, coor, cmp, nmodes):
    # set the figure parameters
    if len(nmodes) %2 == 0:
        print(str(len(nmodes))+' is even!')
    else:
        print(str(len(nmodes))+' is odd!')
    r = int(input('Rows: '))
    c = int(input('Columns: '))
    xmin = np.min(coor[:,0])
    xmax = np.max(coor[:,0])
    ymin = np.min(coor[:,1])
    ymax = np.max(coor[:,1])
    row, col = np.mgrid[ymin:ymax:120j, xmin:xmax:320j]
    fig = plt.figure()
    for i in range(len(nmodes)):
        intp = griddata(coor, data[:,nmodes[i]], (col, row), method='linear')
        sub = fig.add_subplot(r, c, i+1)
        sub.set_title('mode ' + str(nmodes[i])+'('+str(1+i)+')')
        img = sub.imshow(intp, origin='upper', cmap=cmp, extent=[xmin, xmax, ymin, ymax],
                         vmin = -0.05, vmax = 0.05)
    fig.subplots_adjust(right=0.8)
    cbar_ax = fig.add_axes([0.85, 0.15, 0.01, 0.7])
    cbar = plt.colorbar(img, cax=cbar_ax, extend='both', orientation='vertical')
    cbar.set_label(r"$\phi(\xi)$"+ " [-]")
    
def plot_eigs_cplane(eigs, amp, ID, IDF, cmp):
    # draw a circle
    theta = np.arange(0,101,1)*2*np.pi/100
    # complex-plane amplitude plot
    plt.figure()
    plt.grid(b='True', which='both', color='k', linestyle='--', linewidth=0.25)
    plt.plot(np.cos(theta), np.sin(theta), 'k--', linewidth=0.35)
    plt.scatter(eigs.real[ID], eigs.imag[ID], s=np.abs(amp)[ID], 
                c=np.abs(amp[ID]), cmap=cmp, alpha=0.6)
    for i in range(len(IDF)):
        plt.text(eigs.real[IDF[i]], eigs.imag[IDF[i]], str(IDF[i])+'('+str(1+i)+')', fontsize=10)
    cbar = plt.colorbar(extend='both', orientation='vertical')
    cbar.set_label("|b| [-]")
    # comment out limits for full spectrum
    plt.xlim(-1, 1)
    plt.ylim(0, 1)
    plt.xlabel('real[$\mu$]')
    plt.ylabel('imag[$\mu$]')

def plot_freq_domain(freq, amp, ID, IDF):  
    # Amplitide-Frequency plot    
    plt.figure()
    plt.stem(freq[ID], np.abs(amp)[ID], linefmt=':', use_line_collection='TRUE')
    for i in range(len(IDF)):
        plt.text(0.5+freq[IDF[i]], np.abs(amp)[IDF[i]], str(IDF[i])+'('+str(1+i)+')', fontsize=10)
    plt.ylabel('Amplitude [-]')
    plt.xlabel('Frequency [Hz]')

def plot_abs_drate(ID, IDF, sigma):
    # absolute damping rate plot
    plt.figure()
    plt.stem(ID, sigma[ID])
    for i in range(len(IDF)):
        plt.text(0.5+IDF[i], sigma[IDF[i]], str(IDF[i])+'('+str(1+i)+')', fontsize=10)
    plt.ylabel(r"$\sigma_i$ [Hz]")
    plt.xlabel(r"Mode $\phi(\xi)_i$[-]")

def plot_rel_drate(IDF, freq, zeta):
    # relative damping rate plot
    plt.figure()
    plt.stem(freq[IDF], zeta[IDF])
    for i in range(len(IDF)):
        plt.text(0.5+freq[IDF[i]], zeta[IDF[i]], str(IDF[i])+'('+str(1+i)+')', fontsize=10)
    plt.ylabel(r"$\zeta_i$ [Hz/rad]")
    plt.xlabel(r"Frequency [Hz]")

def plot_mode_osc(exp_eigs, ID):
    t = np.arange(0, 1, 0.005)
    damp_up = np.exp(exp_eigs.real[ID]*t)
    damp_down = -np.exp(exp_eigs.real[ID]*t)
    oscilation = np.cos(exp_eigs.imag[ID]*t)
    oscilation_damp = np.exp(exp_eigs.real[ID]*t)*np.cos(exp_eigs.imag[ID]*t)
    plt.figure()
    plt.plot(t, damp_up)
    plt.plot(t, damp_down)
    plt.plot(t, oscilation)
    plt.plot(t, oscilation_damp)
    plt.xlabel("time [s]")
    plt.ylabel("Amplitude [-]")

#-----------------PLOTTING FUNCTIONS FOR BASIC DMD ANALYSIS-------------------# 
###############################################################################
"""This set of functions is optimized for a basic DMD analysis without advanced
   features."""

def plot_dmd_modes_basic(data, coor, cmp, nmodes):
    # set the figure parameters
    xmin = np.min(coor[:,0])
    xmax = np.max(coor[:,0])
    ymin = np.min(coor[:,1])
    ymax = np.max(coor[:,1])
    row, col = np.mgrid[ymin:ymax:120j, xmin:xmax:320j]
    fig = plt.figure()
    for i in range(len(nmodes)):
        intp = griddata(coor, data[:,nmodes[i]], (col, row), method='linear')
        sub = fig.add_subplot(4, 2, i+1)
        sub.set_title('mode ' + str(nmodes[i]))
        sub.imshow(intp, origin='upper', cmap=cmp, extent=[xmin, xmax, ymin, ymax],
                         vmin = -0.05, vmax = 0.05)

def plot_eigs_cplane_basic(eigs, amp, cmp):
    # draw a circle
    theta = np.arange(0,101,1)*2*np.pi/100
    # complex-plane amplitude plot
    plt.figure()
    plt.grid(b='True', which='both', color='k', linestyle='--', linewidth=0.25)
    plt.plot(np.cos(theta), np.sin(theta), 'k--', linewidth=0.35)
    plt.scatter(eigs.real, eigs.imag, s=np.abs(amp)*10, 
                c=np.abs(amp), cmap=cmp, alpha=0.6)
    cbar = plt.colorbar(extend='both', orientation='vertical')
    cbar.set_label("|b| [-]")
    plt.xlim(-1, 1)
    plt.ylim(-1, 1)
    plt.xlabel('real[$\mu$]')
    plt.ylabel('imag[$\mu$]')
    
def plot_freq_domain_basic(freq, amp):  
    # Amplitide-Frequency plot    
    plt.figure()
    plt.stem(freq, np.abs(amp), linefmt=':', use_line_collection='TRUE')
    plt.ylabel('Amplitude [-]')
    plt.xlabel('Frequency [Hz]')
    
# some hints!!!
    # vmin = -0.05, vmax = 0.05 can be added after extent above to set colormap boundaries
    # also extent=[-1.5, 24, -5, 5] can be added to represent real X Y range
