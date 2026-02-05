// 플래시 메시지 자동 닫기
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.alert');

    flashMessages.forEach(function(message) {
        setTimeout(function() {
            message.style.opacity = '0';
            message.style.transform = 'translateX(100%)';
            setTimeout(function() {
                message.remove();
            }, 300);
        }, 5000);
    });
});

/* css transition 추가로 더 부드러운 구현 가능
document.addEventListener('DOMContentLoaded', function() {
    const flashMessages = document.querySelectorAll('.alert');

    flashMessages.forEach(function(message) {
        // CSS transition 설정
        message.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
        
        setTimeout(function() {
            message.style.opacity = '0';
            message.style.transform = 'translateX(100%)';
            
            // transitionend 이벤트로 애니메이션 완료 감지 (더 정확함)
            message.addEventListener('transitionend', function() {
                message.remove();
            }, { once: true });  // 한 번만 실행
        }, 5000);
    });
});
*/

// 숫자 입력 필드에 천 단위 구분 쉼표 추가
function formatNumber(input) {
    let value = input.value.replace(/,/g, '');
    if (!isNaN(value) && value !== '') {
        input.value = Number(value).toLocaleString('ko-KR');
    }
}

// 폼 제출 시 쉼표 제거
function removeCommas(form) {
    const numberInputs = form.querySelectorAll('input[type="number"]');
    numberInputs.forEach(function(input) {
        input.value = input.value.replace(/,/g, '');
    });
}