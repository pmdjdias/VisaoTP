
%% kinect a funcionar
close all; clear all ;clear camObject;

colorDevice = imaq.VideoDevice('kinect',1);
depthDevice = imaq.VideoDevice('kinect',2);




step(colorDevice);
step(depthDevice);

colorImage = step(colorDevice);

depthImage = step(depthDevice);


ptCloud = pcfromkinect(depthDevice,depthImage,colorImage);


player = pcplayer(ptCloud.XLimits,ptCloud.YLimits,ptCloud.ZLimits,...
	'VerticalAxis','y','VerticalAxisDir','down');

xlabel(player.Axes,'X (m)');
ylabel(player.Axes,'Y (m)');
zlabel(player.Axes,'Z (m)');

for i = 1:500    
   colorImage = step(colorDevice);  
   depthImage = step(depthDevice);
 
   ptCloud = pcfromkinect(depthDevice,depthImage,colorImage);
    
   view(player,ptCloud);
    time_ply=sprintf('cloud_%s.ply', datestr(now,'dd-mm_HH-MM-SS'));

    Variablein = input('type 1\n( or 0 to quit)','s');
    Variablein = str2num(Variablein);
      if (Variablein == 1)
      disp('gravar point cloud');
      pcwrite(ptCloud,time_ply,"Encoding","binary")
      
      elseif(Variablein ==0)
        disp("closing")
        close all; clear all ;clear camObject;
        return  
      end



end

















