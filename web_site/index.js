const form = document.querySelector('.model-form');
const predictButton = document.querySelector('.model-btn');

const API_URL = 'https://househunt-e297.onrender.com/api/data';

form.addEventListener('submit', async (event) => {
  event.preventDefault();

  const district = document.querySelector('#district').value;
  const rooms = document.querySelector('#rooms').value;
  const area = document.querySelector('#area').value;
  const floor = document.querySelector('#floor').value;

  const requestData = {
    place: district,
    room_number: rooms,
    squares: area,
    floor: floor,
  };

  console.log('Отправка данных: ', requestData);

  try {
    const response = await fetch(API_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    });

    if (response.ok) {
      const result = await response.json();

      alert(`Предсказанная стоимость: ${result.cost} руб.`);
    } else {
      alert('Ошибка при предсказании. Попробуйте позже.');
    }
  } catch (error) {
    console.log(error);
    alert('Не удалось связаться с сервером. Ошибку см. в консоли.');
  }
});
