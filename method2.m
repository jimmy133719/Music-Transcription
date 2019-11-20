clear; close all;
DIR = './';
FILENAME = '6535431996833792.mp3';
[y,fs1] = audioread([DIR FILENAME]);
y = (y(:,1) + y(:,2))/2;
y(length(y)/2:length(y))=[];
fs = 16000;
y = resample(y,fs,fs1);
%% get stft of signal
window = hanning(512);
noverlap = 256;
nfft = 1024;
[s,w,t,p] = spectrogram(y,window,noverlap,nfft,fs,'yaxis'); % s is stft of signal, w is frequnecy, t is time, p is power spectral density 
%{
figure(1)
surf(t, w, 10*log10(p), 'edgecolor', 'none'); axis tight; view(0,90); colorbar; colormap(hot); 
xlabel("Time(s)"); ylabel("Frequency(Hz)"); title("Spectrogram(Original)");
%}
%% get piano frequency
keys = [];
level = (2)^(1/12);
for n = 1:88 
    key = ((level)^(n-49))*440;
    keys(n) = key;
end


%% frame segment and find corresponding piano frequency
% tempo = 100; %bpm
% tempo = tempo/60; %bps
% framelen = 1/tempo*fs;

% find peak frequency of each time bin
max_freq = zeros(1,length(t)); %這裡可以改多音
bw=3;%stopband width
plot(w,p(:,62));hold on
for k=1:size(max_freq,1)
    for i = 1:size(p,2) %length(t)
        [max_p,index] = findMax( p(:,i) , k);
        max_freq(k,i) = w(index);
        lb=max([index-bw 1]);
        ub=min([index+bw length(w)]);
        p(lb:ub,i) = zeros(ub-lb+1,1);
        plot(w,p(:,62));hold on
    end
end
legend("ori","1","2","3")

% find the nearest piano frequency of each peak frequency 
key_num = zeros(size(max_freq,1),length(t));
for i = 1:length(t)
    for k=1:size(max_freq,1)
        min_error = abs(max_freq(k,i)-max(keys)); 
        for j = 1:length(keys)
            if abs(max_freq(k,i)-keys(j)) < min_error
                min_error = abs(max_freq(k,i)-keys(j));
                key_num(k,i) = j;
            end
        end
    end
end
%% determine the tempo of the song

fftpoint = 2^13; %音檔很長時可以改小
%fratio = fs / fftpoint;
y_fft = fft( y(1:fftpoint) );
%plot( (1:fftpoint/2)*2/fftpoint , abs( y_fft(1:fftpoint/2) ) )


%% output frequency component

frequency=zeros(size(max_freq,1),length(t));
for i=1:size(max_freq,1)
    for j=1:length(t)
        frequency(i,j)=keys( key_num(i,j) );
    end
end
csvwrite('output.csv',frequency);
%}
%%
[peak,beat_length]=findpeaks(sum(p));

   