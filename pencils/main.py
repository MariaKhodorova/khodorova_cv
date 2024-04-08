import cv2
from scipy.spatial import distance

count = 0

for img in range(1, 13):
    raw = cv2.imread(f"pencils/images/img ({img}).jpg")
    image = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(image, 120, 255, 0)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    pencils = 0
    for cnt in contours:
        x, y, w, h = cv2.boundingRect(cnt)
        points = cv2.boxPoints(cv2.minAreaRect(cnt))
        width = distance.euclidean(points[0], points[1])
        high = distance.euclidean(points[0], points[3])
        if (high > 3 * width and high > 1000) or (width > 3 * high and width > 1000):
            pencils += 1
            count += 1
    print(f"Количество карандашей на {img} изображении:", pencils)

print("Суммарное количество карандашей на изображениях:", count)